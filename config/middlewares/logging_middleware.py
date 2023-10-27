import re
import logging

from django import VERSION as django_version
from django.conf import settings

from config.logging import CustomColourLogger


DEFAULT_LOG_LEVEL = logging.DEBUG
IS_DJANGO_VERSION_GTE_3_2_0 = django_version >= (3, 2, 0, "final", 0)
DEFAULT_SENSITIVE_HEADERS = (
    ["Authorization", "Proxy-Authorization"]
    if IS_DJANGO_VERSION_GTE_3_2_0
    else ["HTTP_AUTHORIZATION", "HTTP_PROXY_AUTHORIZATION"]
)

BINARY_REGEX = re.compile(r"(.+Content-Type:.*?)(\S+)/(\S+)(?:\r\n)*(.+)", re.S | re.I)
BINARY_TYPES = ("image", "application")

request_logger = logging.getLogger("django.request")


class LoggingMiddleware(object):
    def __init__(self, get_response=None):
        # ensure that all the member references of LoggingMiddleware are read-only after construction
        # no other methods/properties invocations mutate these references so they can be safely read from any thread
        # https://stackoverflow.com/questions/6214509/is-django-middleware-thread-safe
        # https://stackoverflow.com/questions/10763641/is-this-django-middleware-thread-safe
        # https://blog.roseman.org.uk/2010/02/01/middleware-post-processing-django-gotcha/
        self.get_response = get_response

        self.log_level = logging.DEBUG
        self.sensitive_headers = getattr(
            settings, "REQUEST_LOGGING_SENSITIVE_HEADERS", DEFAULT_SENSITIVE_HEADERS
        )
        if not isinstance(self.sensitive_headers, list):
            raise ValueError(
                "{} should be list. {} is not list.".format(
                    "REQUEST_LOGGING_SENSITIVE_HEADERS", self.sensitive_headers
                )
            )

        self.max_body_length = 50000
        self.logger = CustomColourLogger(request_logger)

    def __call__(self, request):
        # cache in a local reference (instead of a member reference) and then pass in as argument
        # in order to avoid other threads overwriting the original self.cached_request_body reference,
        # is this done to preserve the original value in case it is mutated during the get_response invocation?
        cached_request_body = request.body
        response = self.get_response(request)
        self.process_request(request, response, cached_request_body)
        self.process_response(request, response)
        return response

    def process_request(self, request, response, cached_request_body):
        method_path = "{} [{}] {}".format(
            request.method, request.id, request.get_full_path()
        )
        logging_context = self._get_logging_context(request, None)

        log_level = self.log_level
        if response is not None and response.status_code >= 400:
            log_level = logging.ERROR

        self.logger.log(logging.INFO, method_path, logging_context)
        self._log_request_headers(request, logging_context, log_level)
        self._log_request_body(request, logging_context, log_level, cached_request_body)

    def _log_request_headers(self, request, logging_context, log_level):
        if IS_DJANGO_VERSION_GTE_3_2_0:
            headers = {
                k: v if k not in self.sensitive_headers else "*****"
                for k, v in request.headers.items()
            }
        else:
            headers = {
                k: v if k not in self.sensitive_headers else "*****"
                for k, v in request.META.items()
                if k.startswith("HTTP_")
            }

        if headers:
            self.logger.log(log_level, headers, logging_context)

    def _log_request_body(
        self, request, logging_context, log_level, cached_request_body
    ):
        if cached_request_body is not None:
            content_type = request.META.get("CONTENT_TYPE", "")
            is_multipart = content_type.startswith("multipart/form-data")
            if is_multipart:
                multipart_boundary = (
                    "--" + content_type[30:]
                )  # First 30 characters are "multipart/form-data; boundary="
                self._log_multipart(
                    self._chunked_to_max(cached_request_body),
                    logging_context,
                    log_level,
                    multipart_boundary,
                )
            else:
                self.logger.log(
                    log_level,
                    self._chunked_to_max(cached_request_body),
                    logging_context,
                )

    def process_response(self, request, response):
        resp_log = "{} [{}] {} - {}".format(
            request.method, request.id, request.get_full_path(), response.status_code
        )
        logging_context = self._get_logging_context(request, response)

        if response.status_code >= 400:
            self.logger.log_error(logging.INFO, resp_log, logging_context)
            self._log_resp(logging.ERROR, response, logging_context)
        else:
            self.logger.log(logging.INFO, resp_log, logging_context)
            self._log_resp(self.log_level, response, logging_context)

        return response

    def _get_logging_context(self, request, response):
        """
        Returns a map with args and kwargs to provide additional context to calls to logging.log().
        This allows the logging context to be created per process request/response call.
        """
        return {
            "args": (),
            "kwargs": {"extra": {"request": request, "response": response}},
        }

    def _log_multipart(self, body, logging_context, log_level, multipart_boundary):
        """
        Splits multipart body into parts separated by "boundary", then matches each part to BINARY_REGEX
        which searches for existence of "Content-Type" and capture of what type is this part.
        If it is an image or an application replace that content with "(binary data)" string.
        This function will log "(multipart/form)" if body can't be decoded by utf-8.
        """
        try:
            body_str = body.decode()
        except UnicodeDecodeError:
            self.logger.log(log_level, "(multipart/form)", logging_context)
            return

        parts = body_str.split(multipart_boundary)
        last = len(parts) - 1
        for i, part in enumerate(parts):
            if "Content-Type:" in part:
                match = BINARY_REGEX.search(part)
                if (
                    match
                    and match.group(2) in BINARY_TYPES
                    and not match.group(4) in ("", "\r\n")
                ):
                    part = match.expand(r"\1\2/\3\r\n\r\n(binary data)\r\n")

            if i != last:
                part = part + multipart_boundary

            self.logger.log(log_level, part, logging_context)

    def _log_resp(self, level, response, logging_context):
        if re.match("^application/json", response.get("Content-Type", ""), re.I):
            if IS_DJANGO_VERSION_GTE_3_2_0:
                response_headers = response.headers
            else:
                response_headers = response._headers
            self.logger.log(level, response_headers, logging_context)
            if response.streaming:
                # There's a chance that if it's streaming it's because large and it might hit
                # the max_body_length very often. Not to mention that StreamingHttpResponse
                # documentation advises to iterate only once on the content.
                # So the idea here is to just _not_ log it.
                self.logger.log(level, "(data_stream)", logging_context)
            else:
                self.logger.log(
                    level, self._chunked_to_max(response.content), logging_context
                )

    def _chunked_to_max(self, msg):
        return msg[: self.max_body_length]
