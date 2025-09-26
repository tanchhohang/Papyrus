from django.apps import AppConfig


class PapyrusApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'papyrus_api'

    def ready(self):
        from . import signals
