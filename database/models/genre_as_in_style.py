from django.db import models

from database.models.custom_base_model import CustomBaseModel


class GenreAsInStyle(CustomBaseModel):
    """
    Represents a musical genre (style)
    """
    name = models.CharField(max_length=200, blank=False,
                            help_text='The name of the GenreAsInStyle')

    def __str__(self):
        return "{0}".format(self.name)

    def count(self):
        return self.style.count()

    class Meta(CustomBaseModel.Meta):
        db_table = 'genre_as_in_style'
