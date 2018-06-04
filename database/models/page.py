from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Page(CustomBaseModel):
    page_number = models.PositiveIntegerField()


    class Meta(CustomBaseModel.Meta):
        db_table = 'page'
