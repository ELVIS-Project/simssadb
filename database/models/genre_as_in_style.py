"""Defines a GenreAsInStyle model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class GenreAsInStyle(CustomBaseModel):
    """Represents a musical genre as in style (Classical, Blues, Pop)

    Attributes
    ----------
    name : models.CharField
        The name of this style

    musical_works : models.models.fields.related_descriptors.ManyToManyDescriptor
        References to the MusicalWorks of this style
    """

    name = models.CharField(
        max_length=200, blank=False, help_text="The name of the GenreAsInStyle"
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "genre_as_in_style"
        verbose_name_plural = "Genres as in Style"

    def __str__(self):
        return self.name
