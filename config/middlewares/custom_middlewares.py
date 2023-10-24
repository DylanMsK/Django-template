import uuid
from time import process_time_ns


class CustomMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.id = uuid.uuid4().hex

        start_time = process_time_ns()
        response = self.get_response(request)
        end_time = process_time_ns()

        response["X-Runtime"] = (end_time - start_time) // 1000
        response["X-Request-ID"] = request.id
        return response
