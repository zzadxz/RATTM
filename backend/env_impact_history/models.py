# env_impact_history/models.py
from django.db import models

class EnvImpactHistory(models.Model):
    user_id = models.CharField(max_length=255)
    date = models.DateTimeField()
    company_name = models.CharField(max_length=255)
    env_score = models.FloatField()
    normalized_env_score = models.FloatField()
    env_grade = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user_id} - {self.company_name}: {self.impact_score}"