from django.apps import AppConfig


class EsgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'esg'
    
    def ready(self):
        from utils.firebase import db