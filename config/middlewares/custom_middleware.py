from time import process_time

from rest_framework.request import Request


class CustomMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        start_time = process_time()
        response = self.get_response(request)
        end_time = process_time()

        response["X-Runtime"] = round((end_time - start_time) * 1000)
        response["X-Request-ID"] = request.id
        return response
