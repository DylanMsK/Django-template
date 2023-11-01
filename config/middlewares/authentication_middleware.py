from django.conf import settings
from django.utils.functional import SimpleLazyObject
from rest_framework.request import Request

from core.models import TokenUser


AUTH_URL = getattr(settings, "AUTH_URL", None)


def get_user(request, token):
    if not hasattr(request, "_cached_user"):
        request._cached_user = TokenUser(token)
    return request._cached_user


class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        self.process_request(request)

        response = self.get_response(request)

        return response

    def process_request(self, request: Request):
        request.user = SimpleLazyObject(lambda: get_user(request))
