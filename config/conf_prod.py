import os

from .settings import *

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = False

del STATICFILES_DIRS
STATIC_ROOT = BASE_DIR / "static"