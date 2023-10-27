import re
import logging

from django.utils.termcolors import colorize


class CustomLogger:
    def __init__(self, logger):
        self.logger = logger

    def log(self, level, msg, logging_context):
        args = logging_context["args"]
        kwargs = logging_context["kwargs"]
        for line in re.split(r"\r?\n", str(msg)):
            self.logger.log(level, line, *args, **kwargs)

    def log_error(self, level, msg, logging_context):
        self.log(level, msg, logging_context)


class CustomColourLogger(CustomLogger):
    def __init__(self, logger, log_colour="green", log_error_colour="red"):
        self.logger = logger
        self.log_colour = log_colour
        self.log_error_colour = log_error_colour

    def log(self, level, msg, logging_context):
        colour = self.log_error_colour if level >= logging.ERROR else self.log_colour
        self._log(level, msg, colour, logging_context)

    def log_error(self, level, msg, logging_context):
        # Forces colour to be log_error_colour no matter what level is
        self._log(level, msg, self.log_error_colour, logging_context)

    def _log(self, level, msg, colour, logging_context):
        args = logging_context["args"]
        kwargs = logging_context["kwargs"]
        for line in re.split(r"\r?\n", str(msg)):
            line = colorize(line, fg=colour)
            self.logger.log(level, line, *args, **kwargs)
