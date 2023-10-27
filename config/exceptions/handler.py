import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from config.exceptions import codes


logger = logging.getLogger("django.request")


def custom_exception_handler(exc, context):
    logger.error("[CUSTOM_EXCEPTION_HANDLER_ERROR]")
    logger.error(f"[{timezone.now()}]")
    logger.error("> exc")
    logger.error(f"{exc}")
    logger.error("> context")
    logger.error(f"{context}")

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data = {
            "code": response.status_code,
            "message": str(exc),
            "timestamp": timezone.now(),
        }
        return response
    else:
        data = {**codes.INTERNER_ERROR, "timestamp": timezone.now()}
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
