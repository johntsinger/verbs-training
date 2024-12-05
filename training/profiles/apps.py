from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "training.profiles"

    def ready(self):
        import training.profiles.signals  # noqa: F401
