from rest_framework.exceptions import APIException
from rest_framework import status


"""
APIException dictionary instance process
For Localization Error Control

아래와 같은 형태 필요
STATUS_RSP_INTERNAL_ERROR = {
    'code': 'internal-error',
    'default_message': 'unknown error occurred.',
    'lang_message': {
        'ko': '알 수 없는 오류.',
        'en': 'unknown error occurred.',
    }
}

CustomDictException(STATUS_RSP_INTERNAL_ERROR, {"키": "내용", "키": "내용"}) 으로 추가 가능
code 부분을 추가적인 내용을 넣는 방식으로 사용
"""


class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "custom_exception"
    default_detail = "Custom exception"


class CustomNotFound(CustomException):
    default_code = "custom_not_found"
    default_detail = "Custom not found"
