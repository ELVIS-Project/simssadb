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

    def works(self):
        """Returns all the works that use this instrument"""
        works = set()
        for section in self.sections():
            for work in section.in_works:
                works.add(work)
        return works

    def _count_sections(self):
        return len(self.sections())

    def _count_works(self):
        return len(self.works())

    def prepare_summary(self):
        summary = {'display': self.__str__(),
                   'url': self.get_absolute_url(),
                   'sections': self._count_sections(),
                   'works': self._count_works()
                   }

    class Meta:
        db_table = 'instrument'
