# flake8: noqa
from config.settings.base import *


DEBUG = False

ALLOWED_HOSTS += env.list("ALLOWED_HOSTS")
