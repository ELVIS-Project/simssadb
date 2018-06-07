from django.db import models


class CustomBaseModel(models.Model):
    """Base model that contains common fields for other models

    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True
        app_label = 'database'
