"""
-----------------------------------------------------------------------------------------------
-> App Configurations
-> App in this context means reusable web app components.
-----------------------------------------------------------------------------------------------

"""
from django.apps import AppConfig

class TransactionConfig(AppConfig):
    name = 'transaction'

    def ready(self):
        from utils.firebase import db