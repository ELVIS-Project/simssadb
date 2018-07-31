from django.db import models

from database.models.custom_base_model import CustomBaseModel


class Instrument(CustomBaseModel):
    """
    An instrument or voice

    A part is written for an instrument or voice, and a symbolic music file
    can specify which instrument or voices it contains
    """
    name = models.CharField(max_length=200,
                            help_text='The name of the Instrument or Voice')

    def __str__(self):
        return "{0}".format(self.name)

    def sections(self):
        """Returns all the sections that use this instrument"""
        sections = set()
        for part in self.part_written_for.all():
            sections.add(part.in_section)
        return sections

    def count_sections(self):
        return len(self.sections())

    def __badge_name(self):
        if self.count_sections() > 1:
            return 'sections'
        else:
            return 'section'

    def _prepare_summary(self):
        summary = {
            'display':     self.__str__(),
            'url':         self.get_absolute_url(),
            'badge_count': self.count_sections(),
            'badge_name':  self.__badge_name()
            }
        return summary

    def get_related(self):
        related = {
            'sections': {
                'list':        list(self.sections()),
                'model_name':  'Sections that use this Instrument',
                'model_count': len(list(self.sections()))
                }
            }

        return related

    def detail(self):
        detail_dict = {
            'title':   self.__str__(),
            'related': self.get_related(),
            }

        return detail_dict

    class Meta:
        db_table = 'instrument'
