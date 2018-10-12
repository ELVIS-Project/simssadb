"""Define a Instrument model"""
from django.apps import apps
from django.db import models
from django.db.models import QuerySet

from database.models.custom_base_model import CustomBaseModel


class Instrument(CustomBaseModel):
    """
    An instrument or voice

    A part is written for an instrument or voice, and a symbolic music file
    can specify which instrument or voices it contains

    Attributes
    ----------
    Instrument.name : models.CharField
        The name of this Instrument

    Instrument.parts : models.ManyToOneRel
        References to Parts that use this Instrument

    Instrument.sym_files : models.ManyToManyRel
        References to SymbolicMusicFiles that specify this Instrument
    """
    name = models.CharField(max_length=200,
                            help_text='The name of the Instrument or Voice')

    class Meta:
        db_table = 'instrument'

    def __str__(self):
        return "{0}".format(self.name)

    @property
    def sections(self) -> QuerySet:
        """Get all the Sections that use this Instrument."""
        section_model = apps.get_model('database', 'section')
        sections = section_model.objects.none()
        for part in self.parts.all():
            sections.union(part.in_section)
        return sections

    @property
    def musical_works(self) -> QuerySet:
        """Get all the MusicalWorks that use this Instrument."""
        work_model = apps.get_model('database', 'musical_work')
        works = work_model.objects.none()
        for section in self.sections:
            works.union(section.musical_work)
        return works
