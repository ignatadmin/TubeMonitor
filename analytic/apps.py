from django.apps import AppConfig


class AnalyticConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analytic'

    def ready(self):
        from . import signals