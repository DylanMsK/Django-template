# flake8: noqa
from config.settings.base import *


DEBUG = True

ALLOWED_HOSTS += env.list("ALLOWED_HOSTS")
