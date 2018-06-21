from django.db import models
from django.urls import reverse


class CustomBaseModel(models.Model):
    """Base model that contains common fields for other models"""
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_reverse_detail_name(self):
        return self.__class__.__name__.lower() + '-detail'

    def get_absolute_url(self):
        return reverse(self.get_reverse_detail_name(), kwargs={'pk': self.pk})

    class Meta:
        abstract = True
        app_label = 'database'
