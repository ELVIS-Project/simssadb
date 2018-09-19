from django.db import models

from database.models.custom_base_model import CustomBaseModel


class GenreAsInType(CustomBaseModel):
    """
    Represents a musical genre as in type of work (Motet, Symphony, Mass)
    """
    name = models.CharField(max_length=200, blank=False,
                            help_text='The name of the GenreAsInStyle')

    class Meta(CustomBaseModel.Meta):
        db_table = 'genre_as_in_type'

    def __str__(self):
        return "{0}".format(self.name)
