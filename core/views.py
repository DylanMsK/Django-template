from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


def sample_get(request):
    return JsonResponse({"status": "ok"})


@csrf_exempt
def sample_post(request):
    data = JSONParser().parse(request)
    return JsonResponse(data)


def sample_error(request):
    raise ZeroDivisionError()
