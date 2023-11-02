import logging

from django.conf import settings
from django.utils.functional import SimpleLazyObject
from rest_framework.request import Request

from rest_framework_simplejwt.authentication import JWTAuthentication

# from config.authentication import JWTAuthentication
from core.models import TokenUser


# logger =


def get_user_jwt(request):
    user_jwt = JWTAuthentication().authenticate(Request(request))
    if user_jwt is not None:
        return user_jwt[0]
    return None


class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        self.process_request(request)

        response = self.get_response(request)

        return response

    def process_request(self, request: Request):
        try:
            user = get_user_jwt(request)
            request.user = user
        except Exception as e:
            pass
