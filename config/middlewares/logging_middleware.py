import re
import uuid
import logging

from django.utils import timezone

from config.logging import CustomColourLogger


DEFAULT_LOG_LEVEL = logging.DEBUG

BINARY_REGEX = re.compile(r"(.+Content-Type:.*?)(\S+)/(\S+)(?:\r\n)*(.+)", re.S | re.I)
BINARY_TYPES = ("image", "application")

request_logger = logging.getLogger("django.request")


class LoggingMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

        self.log_level = logging.DEBUG
        self.sensitive_headers = ["Authorization", "Proxy-Authorization"]

        self.max_body_length = 50000
        self.logger = CustomColourLogger(request_logger)

    def __call__(self, request):
        request.id = uuid.uuid4().hex
        cached_request_body = request.body

        self.process_request(request, cached_request_body)

        response = self.get_response(request)

        self.process_response(request, response)
        return response

    def process_request(self, request, cached_request_body):
        logging_context = self._get_logging_context(request, None)

        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        client_ip = self._get_request_ip(request)
        http_method = request.method
        request_url = request.get_full_path()
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        log_string = f'[{timestamp}] {request.id} {client_ip} "{http_method} {request_url}" {user_agent}'

        self.logger.log(logging.INFO, log_string, logging_context)
        self._log_request_headers(request, logging.DEBUG, logging_context)
        self._log_request_body(request, logging_context, cached_request_body)

    def _log_request_headers(self, request, log_level, logging_context):
        headers = {
            k: v if k not in self.sensitive_headers else "*****"
            for k, v in request.headers.items()
        }
        self.logger.log(log_level, headers, logging_context)

    def _log_request_body(self, request, logging_context, cached_request_body):
        if cached_request_body:
            content_type = request.META.get("CONTENT_TYPE", "")
            is_multipart = content_type.startswith("multipart/form-data")
            if is_multipart:
                multipart_boundary = (
                    "--" + content_type[30:]
                )  # First 30 characters are "multipart/form-data; boundary="
                self._log_multipart(
                    self._chunked_to_max(cached_request_body),
                    logging_context,
                    self.log_level,
                    multipart_boundary,
                )
            else:
                self.logger.log(
                    self.log_level,
                    self._chunked_to_max(cached_request_body),
                    logging_context,
                )

    def process_response(self, request, response):
        logging_context = self._get_logging_context(request, response)

        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        http_method = request.method
        request_url = request.get_full_path()
        runtime = response.headers.get("X-Runtime")
        status_code = response.status_code
        user_id = None
        if hasattr(request, "user"):
            user_id = request.user.id

        log_string = f'[{timestamp}] {request.id} "{http_method} {request_url}" user({user_id}) {status_code} {runtime}'

        if status_code >= 400:
            self.logger.log_error(logging.INFO, log_string, logging_context)
            self._log_resp(logging.ERROR, response, logging_context)
        else:
            self.logger.log(logging.INFO, log_string, logging_context)
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

    def _log_multipart(self, log_level, body, logging_context, multipart_boundary):
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
            response_headers = response.headers

            self.logger.log(logging.DEBUG, response_headers, logging_context)
            if response.streaming:
                self.logger.log(level, "(data_stream)", logging_context)
            else:
                self.logger.log(
                    level, self._chunked_to_max(response.content), logging_context
                )

    def _chunked_to_max(self, msg):
        return msg[: self.max_body_length]

    def _get_request_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
