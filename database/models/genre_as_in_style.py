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

    def get_badge_name(self):
        if self.count() > 1:
            return 'musical works'
        else:
            return 'musical work'

    def _prepare_summary(self):
        summary = {
            'display':     self.__str__(),
            'url':         self.get_absolute_url(),
            'badge_name':  self.get_badge_name(),
            'badge_count': self.count()
            }
        return summary

    def get_related(self):
        related = {
            'musical_works_of_this_style': {
                'list':        self.style.all(),
                'model_name':  'Musical Works of this Style',
                'model_count': self.style.count()
                }
            }

        return related

    def detail(self):
        detail_dict = {
            'title':   self.name,
            'related': self.get_related()
            }

        return detail_dict

    class Meta(CustomBaseModel.Meta):
        db_table = 'genre_as_in_style'
