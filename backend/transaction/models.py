"""
NOT IMPLEMENTED, for storing data
-----------------------------------------------------------------------
-> Note: we can include validation logic in the class to verify 
that the data is clean.
-----------------------------------------------------------------------
"""

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
        return (
            f"{self.transaction_id} - {self.company_name}: ${self.transaction_amount}"
        )

    # Example validation logic
    # def clean(self):
    #     # Example validation: Ensure transaction_amount is positive
    #     if self.transaction_amount <= 0:
    #         raise ValidationError(_('Transaction amount must be positive.'))

    #     # Example validation: Ensure latitude is within valid range
    #     if not (-90 <= self.location_latitude <= 90):
    #         raise ValidationError(_('Latitude must be between -90 and 90 degrees.'))

    #     # Example validation: Ensure longitude is within valid range
    #     if not (-180 <= self.location_longitude <= 180):
    #         raise ValidationError(_('Longitude must be between -180 and 180 degrees.'))
