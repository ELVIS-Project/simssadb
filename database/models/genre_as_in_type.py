"""Define GenreAsInType model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class GenreAsInType(CustomBaseModel):
    """Represents a musical genre as in type of work (Motet, Symphony, Mass)

    Attributes
    ----------
    name : models.CharField
        The name of this type of work

    musical_works : models.models.fields.related_descriptors.ManyToManyDescriptor
        References to the MusicalWorks of this type
    """

    name = models.CharField(
        max_length=200, blank=False, help_text="The name of the GenreAsInStyle"
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "genre_as_in_type"
        verbose_name_plural = "Genres as in Type"

    def __str__(self):
        return self.name
