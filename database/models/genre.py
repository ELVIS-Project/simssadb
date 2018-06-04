from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Genre(CustomBaseModel):
    name = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta(CustomBaseModel.Meta):
        db_table = 'genre'
