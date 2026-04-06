from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.db.models import Sum

from .models import VerificationCode
from .services import (
    VerificationError,
    build_identifier,
    dispatch_verification_code,
    validate_verification_code,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    identifier = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    points_balance = serializers.SerializerMethodField()
    miles_balance = serializers.SerializerMethodField()
    membership_tier = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'identifier', 'email', 'full_name', 'points_balance', 'miles_balance', 'membership_tier')

    def get_identifier(self, obj):
        return obj.username

    def get_full_name(self, obj):
        full_name = obj.get_full_name()
        if full_name:
            return full_name
        if hasattr(obj, 'first_name') and obj.first_name:
            return obj.first_name
        return obj.username

    def get_points_balance(self, obj):
        """积分余额（固定值）"""
        return 320

    def get_miles_balance(self, obj):
        """里数余额（固定值）"""
        return 3200

    def get_membership_tier(self, obj):
        """会员卡等级（固定值）"""
        return '银卡'


class SendOtpSerializer(serializers.Serializer):
    channel = serializers.ChoiceField(choices=VerificationCode.CHANNEL_CHOICES)
    country_code = serializers.CharField(required=False, allow_blank=True, max_length=8)
    phone = serializers.CharField(required=False, allow_blank=True, max_length=32)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate(self, attrs):
        channel = attrs.get('channel')
        email = attrs.get('email')
        phone = attrs.get('phone')
        country_code = attrs.get('country_code')

        if channel == VerificationCode.CHANNEL_EMAIL:
            if not email:
                raise serializers.ValidationError({'email': '请输入有效邮箱'})
        else:
            if not phone:
                raise serializers.ValidationError({'phone': '请输入手机号码'})

        identifier = build_identifier(channel, email=email, country_code=country_code, phone=phone)
        if not identifier:
            raise serializers.ValidationError({'identifier': '账号信息不完整'})

        attrs['identifier'] = identifier
        return attrs

    def send_code(self):
        channel = self.validated_data['channel']
        identifier = self.validated_data['identifier']
        email = self.validated_data.get('email', '')
        phone = self.validated_data.get('phone', '')
        dispatch_verification_code(channel, identifier, email=email, phone=phone)


class RegisterSerializer(serializers.Serializer):
    channel = serializers.ChoiceField(choices=VerificationCode.CHANNEL_CHOICES)
    full_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    country_code = serializers.CharField(required=False, allow_blank=True, max_length=8)
    phone = serializers.CharField(required=False, allow_blank=True, max_length=32)
    email = serializers.EmailField(required=False, allow_blank=True)
    otp = serializers.CharField(write_only=True, max_length=10)
    password = serializers.CharField(write_only=True)
    agree = serializers.BooleanField(required=False, default=False)

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        channel = attrs.get('channel')
        email = attrs.get('email')
        phone = attrs.get('phone')
        country_code = attrs.get('country_code')
        otp = attrs.get('otp', '').strip()

        identifier = build_identifier(channel, email=email, country_code=country_code, phone=phone)
        if not identifier:
            raise serializers.ValidationError({'identifier': '账号信息不完整'})

        if not attrs.get('agree', False):
            raise serializers.ValidationError({'agree': 'Please agree to the terms first.'})

        if User.objects.filter(username__iexact=identifier).exists():
            raise serializers.ValidationError({'identifier': '该账号已注册，请直接登录'})

        if not otp:
            raise serializers.ValidationError({'otp': '请输入验证码'})

        try:
            validate_verification_code(identifier, otp)
        except VerificationError as exc:
            raise serializers.ValidationError({'otp': str(exc)}) from exc

        attrs['identifier'] = identifier
        return attrs

    def create(self, validated_data):
        identifier = validated_data['identifier']
        password = validated_data['password']
        full_name = validated_data.get('full_name', '').strip()
        channel = validated_data.get('channel')
        validated_data.pop('otp', None)
        email = validated_data.get('email', '').strip().lower() if channel == VerificationCode.CHANNEL_EMAIL else ''

        user = User(username=identifier, email=email)

        if hasattr(user, 'full_name'):
            user.full_name = full_name
        else:
            if full_name:
                parts = full_name.split(' ', 1)
                user.first_name = parts[0][:150]
                if len(parts) > 1:
                    user.last_name = parts[1][:150]

        user.set_password(password)
        user.save()
        return user

