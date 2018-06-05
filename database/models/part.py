from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Part(CustomBaseModel):
    title = models.CharField(max_length=200)

    class Meta(CustomBaseModel.Meta):
        db_table = 'part'
