from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.source import Source


class Page(CustomBaseModel):
    """Represents a specific page in a source"""
    page_number = models.PositiveIntegerField()
    page_in_source = models.ForeignKey(Source, on_delete=models.CASCADE,
                                       related_name='pages', null=False)

    def __str__(self):
        return "Page {0} of ".format(self.page_number,
                                     self.page_in_source.title)


    class Meta(CustomBaseModel.Meta):
        db_table = 'page'
