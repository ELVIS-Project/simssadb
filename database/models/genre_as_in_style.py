"""Define a GenreAsInStyle model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class GenreAsInStyle(CustomBaseModel):
    """
    Represents a musical genre as in style (Classical, Blues, Pop)

    Attributes
    ----------
    GenreAsInStyle.name : models.CharField
        The name of this style

    GenreAsInStyle.musical_works : models.ManyToManyRel
        References to the MusicalWorks of this style

    See Also
    --------
    database.models.CustomBaseModel
    database.models.MusicalWork
    """

    name = models.CharField(
        max_length=200, blank=False, help_text="The name of the GenreAsInStyle"
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "genre_as_in_style"

    def __str__(self):
        return "{0}".format(self.name)
