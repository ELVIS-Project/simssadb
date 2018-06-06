from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Software(CustomBaseModel):
    name = models.CharField(blank=False, max_length=100)
    version = models.CharField(blank=False, default='1.0', max_length=10)
    configuration_file = models.FileField()


    class Meta(CustomBaseModel.Meta):
        db_table = 'software'
