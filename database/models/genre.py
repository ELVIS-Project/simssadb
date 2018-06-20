from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Genre(CustomBaseModel):
    """Represents a musical genre

    Can be genre as in style (i.e. Classical, Pop, Bluegrass) or genre as in
    type of work (Motet, Symphony, Mass)
    """
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta(CustomBaseModel.Meta):
        db_table = 'genre'
