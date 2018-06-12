from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.musical_work import MusicalWork
from database.models.section import Section
from database.models.part import Part
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField


class Source(CustomBaseModel):
    """Represents a document containing the music defining a specific Instance

    An Instance in turn corresponds to all or part of a Musical Work.
    Can be divided into Pages.
    Can be a component of a Collection of Sources.
    """
    title = models.CharField(max_length=200, blank=False)
    publication_date = models.DateField
    editorial_notes = models.TextField()
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

    # Source can be published by a person or institution
    limit = models.Q(app_label='database', model='person') | models.Q(
            app_label='database', model='institution')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    publisher = GenericForeignKey('content_type', 'object_id')

    work = models.ManyToManyField(MusicalWork)
    section = models.ManyToManyField(Section)
    part = models.ManyToManyField(Part)


    def __str__(self):
        return "{0}".format(self.title)

    class Meta(CustomBaseModel.Meta):
        db_table = 'source'
