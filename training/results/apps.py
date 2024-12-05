from django.apps import AppConfig


class ResultsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "training.results"

    def ready(self):
        import training.results.signals  # noqa: F401
