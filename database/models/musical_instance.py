from django.db import models
from database.models.custom_base_model import CustomBaseModel


class MusicalInstance(CustomBaseModel):
    title = models.CharField(max_length=200)


    class Meta:
        db_table = 'musical_instance'
