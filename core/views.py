from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def sample_error(request):
    # raise NotFound()
    if 5 / 0:
        return Response({})


class SampleGetViewset(APIView):
    def get(self, request):
        print(request.user)
        return Response({"status": "ok"})


class SamplePostViewset(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        return Response(data)
