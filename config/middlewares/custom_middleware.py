import uuid
import requests
from dataclasses import dataclass
from time import process_time_ns

from django.conf import settings
from rest_framework.request import Request
from rest_framework import exceptions


AUTH_URL = getattr(settings, "AUTH_URL", None)


@dataclass(frozen=True)
class Member:
    id: int
    name: str
    role: str = ""


class CustomMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        request.id = uuid.uuid4().hex

        if self.authenticate(request):
            pass

        start_time = process_time_ns()
        response = self.get_response(request)
        end_time = process_time_ns()

        response["X-Runtime"] = (end_time - start_time) // 1000
        response["X-Request-ID"] = request.id
        return response

    def authenticate(self, request: Request) -> bool:
        header = self.get_header(request)
        if header is None:
            raise exceptions.NotAuthenticated()
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def get_member_with_token(self, request: Request):
        headers = self.get_header(request)

    def get_header(self, request: Request) -> bytes:
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get("HTTP_AUTHORIZATION")
        return header
