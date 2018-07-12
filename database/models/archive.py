from cached_property import cached_property
from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.collection_of_sources import CollectionOfSources
from database.models.institution import Institution


class Archive(CustomBaseModel):
    """
    A location where Sources and Collections of Sources are stored

    e.g: A database or a library
    """
    name = models.CharField(max_length=200, blank=False, null=False,
                            help_text='The name of the Archive')
    collections = models.ManyToManyField(CollectionOfSources,
                                         related_name='in_archive',
                                         help_text='Sources that belong '
                                                   'to this Archive')

    institution = models.ForeignKey(Institution, null=True,
                                    on_delete=models.SET_NULL,
                                    help_text='The Institution that this '
                                              'Archive is part of')

    def __str__(self):
        return "{0}".format(self.name)

    @cached_property
    def summary(self):
        summary = {'display': "{0} part of {1}".format(self.name, self.institution.name),
                   'number_of_collections': self.collections.count()}
        return summary

    class Meta(CustomBaseModel.Meta):
        db_table = 'archive'
