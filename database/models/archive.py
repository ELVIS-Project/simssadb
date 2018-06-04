from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Archive(CustomBaseModel):
    title = models.CharField(max_length=200, blank=False)


    class Meta(CustomBaseModel):
        db_table = 'archive'
