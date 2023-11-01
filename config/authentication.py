from typing import Optional, Tuple
import requests

from rest_framework import authentication
from rest_framework.request import Request
from django.conf import settings

from core.models import TokenUser


AUTH_URL = getattr(settings, "AUTH_URL", None)


class JWTAuthentication(authentication.BaseAuthentication):
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a request header.
    """

    www_authenticate_realm = "api"
    media_type = "application/json"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def authenticate(self, request: Request) -> Optional[Tuple[TokenUser, str]]:
        token = request.META.get("HTTP_AUTHORIZATION")
        header = {"Authorization": token}
        res = requests.get(AUTH_URL, headers=header)
        if res.status_code != 200:
            return None, None

        user = TokenUser(res.json())

        return user, res.json()
