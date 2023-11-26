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
        from django.db import connections
        from django.db.utils import OperationalError

        # 데이터베이스 연결 체크
        db_conn = connections["default"]
        try:
            db_conn.cursor()
        except OperationalError:
            db_status = "disconnected"
        else:
            db_status = "connected"

        service_status = "healthy" if db_status == "connected" else "unhealthy"

        response = {
            "status": service_status,
            "database": db_status,
        }

        return Response(response)


class ProjectInfo(APIView):
    def get(self, request):
        config = configparser.ConfigParser()
        config.read(settings.BASE_DIR / "pyproject.toml")
        response = {
            "name": config.get("tool.poetry", "name").strip('"'),
            "version": config.get("tool.poetry", "version").strip('"'),
        }
        return Response(response)
