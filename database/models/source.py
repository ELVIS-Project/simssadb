from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.musical_work import MusicalWork
from database.models.section import Section
from database.models.part import Part
from django.contrib.postgres.fields import ArrayField
from database.models.collection_of_sources import CollectionOfSources


class Source(CustomBaseModel):
    """Represents a document containing the music defining a specific Instance

    Can be a component of a Collection of Sources.
    """
    languages = ArrayField(models.CharField(max_length=200, blank=True),
                           blank=True, null=True)
    work = models.ForeignKey(MusicalWork, null=False, blank=False,
                             on_delete=models.PROTECT)
    sections = models.ManyToManyField(Section)
    parts = models.ManyToManyField(Part)
    part_of_collection = models.ForeignKey(CollectionOfSources, null=False,
                                           blank=False,
                                           on_delete=models.PROTECT)
    parent_sources = models.ManyToManyField('self',
                                            related_name='child_sources',
                                            blank=True)
    portion = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.part_of_collection.title)


    class Meta(CustomBaseModel.Meta):
        db_table = 'source'
