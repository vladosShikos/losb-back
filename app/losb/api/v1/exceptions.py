from rest_framework.exceptions import APIException

class BirthdayAlreadyRegistered(APIException):
    status_code = 409
    default_detail = 'A birthday has already been set for this account.'


# TODO: add default detail
# POST phone
class PhoneAlreadyVerified(APIException):
    status_code = 409
    default_detail = ''

class SmsVerificationResendCooldown(APIException):
    status_code = 403
    default_detail = 'You must wait for the specified time period before requesting a new SMS verification code.'

# PUT phone
class SmsVerificationNotSend(APIException):
    status_code = 409
    default_detail = ''

class SmsVerificationExpired(APIException):
    status_code = 403
    default_detail = ''

class SmsVerificationAttemptsExceeded(APIException):
    status_code = 403
    default_detail = ''

class SmsVerificationFailed(APIException):
    status_code = 403
    default_detail = ''
