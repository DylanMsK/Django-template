from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from rest_framework.response import Response


def sample_error(request):
    raise ValidationError()
    raise Http404()
    raise ZeroDivisionError()


class SampleGetViewset(APIView):
    def get(self, request):
        return Response({"status": "ok"})


class SamplePostViewset(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        raise ParseError()
        return Response(data)
