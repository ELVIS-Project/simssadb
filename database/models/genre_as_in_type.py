from django.db import models

from database.models.custom_base_model import CustomBaseModel


class GenreAsInType(CustomBaseModel):
    """
    Represents a musical genre as in type

    Can be genre as in style (i.e. Classical, Pop, Bluegrass) or genre as in
    type of work (Motet, Symphony, Mass)
    """
    name = models.CharField(max_length=200, blank=False,
                            help_text='The name of the GenreAsInStyle')

    def __str__(self):
        return "{0}".format(self.name)

    def count(self):
        return self.type.count()

    class Meta(CustomBaseModel.Meta):
        db_table = 'genre_as_in_type'
