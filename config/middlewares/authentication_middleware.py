import requests

from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.http.response import JsonResponse
from rest_framework.request import Request


AUTH_URL = getattr(settings, "AUTH_URL", None)


class Member(AnonymousUser):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @property
    def is_authenticated(self):
        return True


class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        token = request.META.get("HTTP_AUTHORIZATION")
        header = {"Authorization": token}
        res = requests.get(AUTH_URL, headers=header)
        if res.status_code != 200:
            return JsonResponse(res.json(), status=res.status_code)

        response = self.get_response(request)

        return response
