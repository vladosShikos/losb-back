from rest_framework.exceptions import APIException

class BirthdayAlreadyRegistered(APIException):
    status_code = 409
    default_detail = 'A birthday has already been set for this account.'


# TODO: add default detail
# POST phone
# TODO: make exception details less explicit for security sake (leaks a lot of info rn)
class PhoneAlreadyVerified(APIException):
    status_code = 409
    default_detail = 'Trying to verify already registered phone number.'

class SmsVerificationResendCooldown(APIException):
    status_code = 403
    default_detail = f'You must wait for N seconds before requesting a new SMS verification code.' # TDOO update message

# PUT phone
class SmsVerificationNotSend(APIException):
    status_code = 409
    default_detail = 'Sms verification was not issued.'

class SmsVerificationExpired(APIException):
    status_code = 403
    default_detail = 'Sms verification code expired.'

class SmsVerificationAttemptsExceeded(APIException):
    status_code = 403
    default_detail = 'Sms verification attempts exceeded.'

class SmsVerificationFailed(APIException):
    status_code = 403
    default_detail = 'Sms verification failed'

class SmsDeliveryError(APIException):
    def __init__(self, default_detail):
        self.default_detail = default_detail