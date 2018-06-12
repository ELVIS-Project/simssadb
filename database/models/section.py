from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.contenttypes.fields import GenericRelation
from database.models.part import Part
from database.models.contributed_to import ContributedTo


class Section(CustomBaseModel):
    """A component of a Musical Work e.g. an Aria in an Opera

    Can alternatively be a Musical Work in its entirety.
    A purely abstract entity that can manifest in differing version.
    Can exist in more than one Musical Work.
    Divided into one or more parts.
    Must have at least one part.
    """
    title = models.CharField(max_length=200)
    ordering = models.PositiveIntegerField()
    section_of = models.ManyToManyField('self', related_name='in_sections',
                                        blank=True)
    parts = models.ManyToManyField(Part, related_name='in_sections')

    def __str__(self):
        return "{0}".format(self.title)


    class Meta(CustomBaseModel.Meta):
        db_table = 'section'
