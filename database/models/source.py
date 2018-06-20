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
    title = models.CharField(max_length=200, blank=False)
    languages = ArrayField(
            ArrayField(
                    models.CharField(max_length=200, blank=True)
            ),
            blank=True, null=True
    )

    PHYSICAL = 'p'
    ELECTRONIC = 'e'
    PHYSICAL_OR_ELECTRONIC = (
        (PHYSICAL, 'Physical'),
        (ELECTRONIC, 'Electronic')
    )
    physical_or_electronic = models.CharField(max_length=1,
                                              choices=PHYSICAL_OR_ELECTRONIC,
                                              default=PHYSICAL)
    work = models.ManyToManyField(MusicalWork)
    section = models.ManyToManyField(Section)
    part = models.ManyToManyField(Part)
    part_of_collection = models.ForeignKey(CollectionOfSources, null=False,
                                           blank=False,
                                           on_delete=models.PROTECT)
    parent_sources = models.ManyToManyField('self',
                                            related_name='child_sources',
                                            blank=True)

    def __str__(self):
        return "{0}".format(self.title)


    class Meta(CustomBaseModel.Meta):
        db_table = 'source'
