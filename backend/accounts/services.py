import logging
import random
import sys
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import VerificationCode

logger = logging.getLogger(__name__)


def build_identifier(channel, email='', country_code='', phone=''):
    if channel == VerificationCode.CHANNEL_EMAIL:
        return (email or '').strip().lower()
    country = (country_code or '').strip()
    phone_number = (phone or '').strip()
    return f'{country}{phone_number}'


def generate_code(length=6):
    digits = '0123456789'
    return ''.join(random.choice(digits) for _ in range(length))


def create_verification_code(identifier, channel, ttl_minutes=5, length=6):
    code = generate_code(length)
    expires_at = timezone.now() + timedelta(minutes=ttl_minutes)
    VerificationCode.objects.update_or_create(
        identifier=identifier,
        defaults={
            'channel': channel,
            'code': code,
            'expires_at': expires_at,
            'attempts': 0,
            'is_active': True,
        },
    )
    return code, expires_at


def send_email_code(email, code, expires_at):
    subject = _('您的验证码')
    message = _('您的验证码为 {code}，有效期至 {time}。').format(
        code=code,
        time=expires_at.strftime('%H:%M'),
    )
    
    # 控制台输出 - 会显示在Django runserver的终端中
    print("\n" + "="*60)
    print("📧 邮箱验证码")
    print(f"收件人: {email}")
    print(f"验证码: {code}")
    print(f"有效期至: {expires_at.strftime('%H:%M')}")
    print("="*60 + "\n")
    sys.stdout.flush()  # 强制刷新输出缓冲区
    
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)
    except Exception as exc:  # pragma: no cover - 取决于邮件配置
        logger.warning('发送验证码邮件失败：%s', exc)
        # 若邮件配置缺失，至少在日志中记录验证码，便于调试
        logger.info('验证码（调试用途）: %s -> %s', email, code)


def dispatch_verification_code(channel, identifier, email='', phone=''):
    code, expires_at = create_verification_code(identifier, channel)
    if channel == VerificationCode.CHANNEL_EMAIL:
        send_email_code(email, code, expires_at)
    else:
        # 控制台输出短信验证码
        print("\n" + "="*60)
        print("📱 短信验证码")
        print(f"手机号: {identifier}")
        print(f"验证码: {code}")
        print(f"有效期至: {expires_at.strftime('%H:%M')}")
        print("="*60 + "\n")
        sys.stdout.flush()  # 强制刷新输出缓冲区
        logger.info('短信验证码（调试用途）: %s -> %s', identifier, code)
    return code


class VerificationError(Exception):
    pass


def validate_verification_code(identifier, submitted_code):
    try:
        record = VerificationCode.objects.get(identifier=identifier)
    except VerificationCode.DoesNotExist as exc:
        raise VerificationError(_('验证码无效或已过期')) from exc

    if not record.is_active or record.is_expired():
        record.delete()
        raise VerificationError(_('验证码无效或已过期'))

    if record.code != (submitted_code or '').strip():
        record.attempts += 1
        record.save(update_fields=['attempts'])
        raise VerificationError(_('验证码不正确'))

    record.is_active = False
    record.save(update_fields=['is_active'])
    return True

