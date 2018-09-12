from database.models import CustomBaseModel
from django.db import models


class Source(CustomBaseModel):

    collection = models.ForeignKey('CollectionOfSources',
                                   null=False,
                                   blank=False,
                                   on_delete=models.PROTECT,
                                   related_name='sources')
    parent_source = models.ForeignKey('self',
                                      null=True,
                                      blank=True,
                                      on_delete=models.PROTECT,
                                      related_name='child_sources')

    class Meta(CustomBaseModel.Meta):
        db_table = 'source'
