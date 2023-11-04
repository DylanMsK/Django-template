import logging

from django.utils import timezone
from rest_framework.views import exception_handler as origin_exception_handler
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken

from core.exceptions import CustomException


logger = logging.getLogger("django.request")


def exception_handler(exc, context):
    data = {
        "error": {},
        "timestamp": timezone.now(),
    }

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = origin_exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        error = {
            "code": f"ERR{response.status_code}",
            "msg": "",
        }
        if isinstance(exc, InvalidToken):
            msg = exc.detail
        elif isinstance(exc, exceptions.ParseError):
            msg = exc.detail
        elif isinstance(exc, exceptions.AuthenticationFailed):
            msg = exc.detail
        elif isinstance(exc, exceptions.NotAuthenticated):
            msg = exc.detail
        elif isinstance(exc, exceptions.PermissionDenied):
            msg = exc.detail
        elif isinstance(exc, exceptions.NotFound):
            msg = exc.detail
        elif isinstance(exc, exceptions.MethodNotAllowed):
            msg = exc.detail
        elif isinstance(exc, exceptions.NotAcceptable):
            msg = exc.detail
        elif isinstance(exc, exceptions.UnsupportedMediaType):
            msg = exc.detail
        elif isinstance(exc, exceptions.Throttled):
            msg = exc.detail
        elif isinstance(exc, exceptions.ValidationError):
            msg = exc.detail
        elif isinstance(exc, CustomException):
            error["code"] = exc.default_code
            msg = exc.detail
        else:
            msg = "Unknown error"

        error["msg"] = msg
        data["error"] = error
        response.data = data

        return response

    data["error"] = {
        "code": "ERR500",
        "message": "Unknown error",
    }
    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
