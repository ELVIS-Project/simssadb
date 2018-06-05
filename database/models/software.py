from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Software(CustomBaseModel):
    name = models.CharField(blank=False)
    version = models.CharField(blank=False, default='1.0')
    configuration_file = models.FileField()


    class Meta(CustomBaseModel.Meta):
        db_table = 'software'
