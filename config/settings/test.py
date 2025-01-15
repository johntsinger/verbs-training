"""Django tests environment settings."""

from .base import *


ROOT_URLCONF = "config.urls.test"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Email configs

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

# Tests

# TEST_RUNNER = 'config.tests.runner.MyTestRunner'
IS_TEST = True
