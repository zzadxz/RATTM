from django.db import models

# define columns -> then we get actual data from Firebase?
class Transaction(models.Model):
    transaction_id = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    date = models.DateTimeField()
    company_name = models.CharField(max_length=255) 
    location_latitude = models.FloatField()  
    location_longitude = models.FloatField() 
    transaction_amount = models.FloatField() 

    def __str__(self):
        return f"{self.transaction_id} - {self.company_name}: ${self.transaction_amount}"