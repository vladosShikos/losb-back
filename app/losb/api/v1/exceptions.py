from rest_framework.exceptions import APIException

class BdayAlreadySet(APIException):
    status_code = 409
    default_detail = 'User birthday is already set'