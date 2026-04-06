from django.db import models
from django.utils import timezone


class VerificationCode(models.Model):
    CHANNEL_EMAIL = 'email'
    CHANNEL_PHONE = 'phone'
    CHANNEL_CHOICES = (
        (CHANNEL_EMAIL, 'Email'),
        (CHANNEL_PHONE, 'Phone'),
    )

    identifier = models.CharField(max_length=150, unique=True, db_index=True)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    code = models.CharField(max_length=10)
    expires_at = models.DateTimeField()
    attempts = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f'{self.identifier} - {self.code}'

