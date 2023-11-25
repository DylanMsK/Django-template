import configparser

from django.conf import settings
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.exceptions import CustomNotFound


@api_view(["GET"])
def sample_error(request):
    if 5 / 0:
        return Response({})


class SamplePostViewset(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        return Response(data)


class SampleFormDataViewset(APIView):
    pass


class HealthCheck(APIView):
    def get(self, request):
        return Response({"status": "ok"})


class ProjectInfo(APIView):
    def get(self, request):
        config = configparser.ConfigParser()
        config.read(settings.BASE_DIR / "pyproject.toml")
        data = {
            "name": config.get("tool.poetry", "name").strip('"'),
            "version": config.get("tool.poetry", "version").strip('"'),
        }
        return Response(data)
