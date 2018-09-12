from django.contrib.postgres.fields import ArrayField
from django.db import models

from database.mixins.file_and_source_info_mixin import FileAndSourceInfoMixin
from database.models.custom_base_model import CustomBaseModel
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.genre_as_in_type import GenreAsInType
from database.models.instrument import Instrument


class MusicalWork(FileAndSourceInfoMixin, CustomBaseModel):
    """
    A complete work of music

    A purely abstract entity that can manifest in differing versions.
    Divided into sections.
    Must have at least one section.
    """
    variant_titles = ArrayField(
            models.CharField(max_length=200, blank=True),
            blank=False, null=False, default=['hello', 'world'],
            help_text='All the titles commonly attributed to this '
                      'musical work. Include the opus or catalogue number '
                      'if there is one.')

    genres_as_in_style = models.ManyToManyField(GenreAsInStyle,
                                                related_name='style',
                                                help_text='e.g., classical, '
                                                          'pop, folk')
    genres_as_in_type = models.ManyToManyField(GenreAsInType,
                                               related_name='type',
                                               help_text='e.g., sonata, motet, '
                                                         '12-bar blues')

    _sacred_or_secular = models.NullBooleanField(null=True, blank=True,
                                                 default=None,
                                                 help_text='Leave blank if not '
                                                           'applicable.')
    authority_control_url = models.URLField(null=True, blank=True,
                                            help_text='URI linking to an '
                                                      'authority control '
                                                      'description of this '
                                                      'musical work.')
    authority_control_key = models.IntegerField(unique=True, blank=True,
                                                null=True,
                                                help_text='The identifier of '
                                                          'this musical work '
                                                          'in the authority '
                                                          'control')
    contributors = models.ManyToManyField(
            'Person',
            through='Contribution',
            through_fields=(
                'contributed_to_work', 'person'),
            help_text='All the people that '
                      'contributed to this '
                      'musical work: e.g., '
                      'composer or arranger')

    class Meta(CustomBaseModel.Meta):
        db_table = 'musical_work'
        verbose_name_plural = 'Musical Works'

    def __str__(self):
        return "{0}".format(self.variant_titles[0])

    @property
    def parts(self):
        """Gets all the Parts related to this Musical Work"""
        parts = []
        for section in self.sections.all():
            parts.extend(section.parts.all())
        return parts

    @property
    def instrumentation(self):
        """Gets all the Instruments used in this Musical Work"""
        instruments = Instrument.objects.none()
        for section in self.sections.all():
            instruments = instruments.union(section.instrumentation)
        return instruments

    @property
    def sacred_or_secular(self):
        if self._sacred_or_secular:
            return 'Sacred'
        if not self._sacred_or_secular:
            return 'Secular'
        if self._sacred_or_secular is None:
            return 'Non Applicable'
