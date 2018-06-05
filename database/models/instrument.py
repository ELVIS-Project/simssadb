from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Instrument(CustomBaseModel):
    name = models.CharField(max_length=200)
    # Maybe add a regex validation here so it looks like 111.111.11
    hb_number = models.CharField(max_length=15)


    class Meta:
        db_table = 'instrument'
