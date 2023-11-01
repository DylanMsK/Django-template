import uuid
from time import process_time_ns

from django.conf import settings
from rest_framework.request import Request


AUTH_URL = getattr(settings, "AUTH_URL", None)


class CustomMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        request.id = uuid.uuid4().hex

        start_time = process_time_ns()
        response = self.get_response(request)
        end_time = process_time_ns()

        response["X-Runtime"] = (end_time - start_time) // 1000
        response["X-Request-ID"] = request.id
        return response

    # def process_exception(self, request, exception):
    #     if isinstance(exception, PermissionDenied):
    #         return HttpResponse(
    #             str(exception), status=status.HTTP_401_UNAUTHORIZED
    #         )  # PermissionDenied가 발생하면 401 상태 코드로 응답

    #     return None
