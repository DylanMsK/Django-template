from rest_framework.exceptions import APIException


class CustomException(APIException):
    status_code = 200
    default_detail = "Unknown Error"
    default_code = "unknown"
