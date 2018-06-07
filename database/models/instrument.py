from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Instrument(CustomBaseModel):
    """An instrument or voice

    A part is written for an instrument or voice, and a symbolic music file
    can specify which instrument or voices it contains
    """
    name = models.CharField(max_length=200)


    class Meta:
        db_table = 'instrument'
