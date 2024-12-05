"""Django local environment settings."""

from dotenv import load_dotenv

from .base import *


load_dotenv(BASE_DIR / ".env")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = ["127.0.0.1"]


# Application definition
INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email configs

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
