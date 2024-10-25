from random import SystemRandom
from django.utils import timezone

from app import settings
from losb.api.v1 import exceptions
from losb.api.v1.serializers import PhoneSerializer, SMSVerificationSerializer


class SmsVerificationService:
    def __init__(self, user):
        self.user = user

    @staticmethod
    def generate_otp():
        return "".join(SystemRandom().choice('123456789') for _ in range(settings.SMS_VERIFICATOIN_CODE_DIGITS))

    def request_verification(self, code, number):
        # Check if phone is already verified
        if (self.user.phone.code == code and self.user.phone.number == number):
            raise exceptions.PhoneAlreadyVerified()

        # Check cooldown period
        self._check_cooldown()

        # Generate and save OTP
        otp = self.generate_otp()
        self._save_verification(otp)

        return otp

    def verify_code(self, phone, code):
        if not self.user.sms_verification:
            raise exceptions.SmsVerificationNotSend()

        if self.user.number == phone:
            raise exceptions.PhoneAlreadyVerified()

        self._check_verification_expiry()
        self._check_verification_attempts()

        if self.user.sms_verification.otp != code:
            self._increment_attempts()
            raise exceptions.SmsVerificationFailed()

        return self._update_phone(phone)

    def _check_cooldown(self):
        if self.user.sms_verification:
            td = timezone.now() - self.user.sms_verification.created_at
            if td.seconds < settings.SMS_VERIFICATION_RESEND_COOLDOWN:
                raise exceptions.SmsVerificationResendCooldown(
                    detail=f'You must wait for {settings.SMS_VERIFICATION_RESEND_COOLDOWN - td.seconds} seconds'
                           f' before requesting a new SMS verification code.'
                )

    def _save_verification(self, otp):
        serializer = SMSVerificationSerializer(data={'otp': otp})
        serializer.is_valid(raise_exception=True)
        self.user.sms_verification = serializer.save()
        self.user.save()

    def _check_verification_expiry(self):
        td = timezone.now() - self.user.sms_verification.created_at
        if td.seconds > settings.SMS_VERIFICATION_RESEND_COOLDOWN:
            self.user.sms_verification.delete()
            raise exceptions.SmsVerificationExpired()

    def _check_verification_attempts(self):
        if self.user.sms_verification.attempts > settings.SMS_VERIFICATION_ATTEMPTS:
            self.user.sms_verification.delete()
            raise exceptions.SmsVerificationAttemptsExceeded()

    def _increment_attempts(self):
        self.user.sms_verification.attempts += 1
        self.user.sms_verification.save()

    def _update_phone(self, phone):
        serializer = PhoneSerializer(data=phone)
        serializer.is_valid(raise_exception=True)

        # TODO: Implement transaction handling here
        self.user.number = serializer.save()
        self.user.save()
        self.user.sms_verification.delete()

        return serializer.data