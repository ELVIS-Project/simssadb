from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.source import Source


class Page(CustomBaseModel):
    """Represents a specific page in a source"""
    page_number = models.PositiveIntegerField()
    page_in_source = models.ForeignKey(Source, on_delete=models.CASCADE,
                                       related_name='pages', null=False)


    class Meta(CustomBaseModel.Meta):
        db_table = 'page'
