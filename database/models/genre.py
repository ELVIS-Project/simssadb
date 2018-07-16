from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Genre(CustomBaseModel):
    """
    Represents a musical genre

    Can be genre as in style (i.e. Classical, Pop, Bluegrass) or genre as in
    type of work (Motet, Symphony, Mass)
    """
    name = models.CharField(max_length=200, blank=False,
                            help_text='The name of the Genre')

    def __str__(self):
        return "{0}".format(self.name)

    def count(self):
        return self.type.count() + self.style.count()

    def get_badge_name(self):
        if self.count() > 1:
            return 'musical works'
        else:
            return 'musical work'

    def prepare_summary(self):
        summary = {'display': self.__str__(),
                   'url': self.get_absolute_url(),
                   'badge_name': self.get_badge_name(),
                   'badge_count': self.count()
                   }
        return summary

    class Meta(CustomBaseModel.Meta):
        db_table = 'genre'
