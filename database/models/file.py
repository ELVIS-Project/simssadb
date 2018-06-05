from django.db import models
from database.models.custom_base_model import CustomBaseModel


class File(CustomBaseModel):
    file_type = models.CharField(max_length=10)
    file_size = models.PositiveIntegerField()
    version = models.CharField(max_length=20, null=True)
    encoding_date = models.DateTimeField(null=True)


    class Meta:
        abstract = True
