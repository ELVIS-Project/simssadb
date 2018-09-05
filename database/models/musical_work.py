from django.contrib.postgres.fields import ArrayField
from django.db import models

import database.mixins.contribution_helper as contribution_helper
from database.mixins.file_and_source_info import FileAndSourceInfoMixin
from database.models.custom_base_model import CustomBaseModel
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.genre_as_in_type import GenreAsInType
from database.models.geographic_area import GeographicArea
from database.models.instrument import Instrument
from database.models.person import Person
from database.models.section import Section
from database.models.symbolic_music_file import SymbolicMusicFile
from database.utils.model_utils import clean_date


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

    sections = models.ManyToManyField(Section, related_name='in_works',
                                      help_text='List all movements or '
                                                'sections here.')

    sacred_or_secular = models.NullBooleanField(null=True, blank=True,
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
            through='ContributedTo',
            through_fields=(
                'contributed_to_work', 'person'),
            help_text='All the people that '
                      'contributed to this '
                      'musical work: e.g., '
                      'composer or arranger')

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
    def certainty_of_attribution(self):
        """Returns True if all the relationships have certain == True"""
        certainties = self.contributed_to.values_list('certain', flat=True)
        if False in certainties:
            return False
        else:
            return True

    @property
    def dates_of_composition(self):
        """Gets the date of contribution of all the composers of this Work"""
        dates = []
        relationships = self.contributed_to.filter(role='COMPOSER')
        for relationship in relationships:
            dates.append(clean_date(relationship.date))
        return dates

    @property
    def places_of_composition(self):
        """Gets the place of contribution of all the composers of this Work"""
        places = GeographicArea.objects.none()
        relationships = self.contributed_to.filter(role='COMPOSER')
        for relationship in relationships:
            places = places.union(GeographicArea.objects.filter(
                    pk=relationship.location_id))
        return places

    def __str__(self):
        return "{0}".format(self.variant_titles[0])

    @staticmethod
    def _composers_for_summary(composers):
        if len(composers) > 1:
            return composers[0]['person'].__str__() + ' and others'
        elif len(composers) == 1:
            return composers[0]['person'].__str__()
        else:
            return "No composer"

    @property
    def composers_queryset(self):
        contributions = self.contributed_to.all().filter(
                role='COMPOSER').prefetch_related('person')
        composers = Person.objects.none()

        for contribution in contributions:
            composers = composers.union(Person.objects.filter(
                    pk=contribution.person_id))

        return composers

    @property
    def composers(self):
        person_ids = self.contributed_to.filter(role='COMPOSER').values_list(
                'person', flat=True)
        return Person.objects.filter(id__in=person_ids)

    @property
    def authors(self):
        contributions = self.contributed_to.all().select_related('person')
        contributions_summaries = \
            contribution_helper.get_contributions_summaries(contributions)
        return contribution_helper.filter_contributions_by_role(
                contributions_summaries, 'author')

    @property
    def get_sacred_or_secular(self):
        if self.sacred_or_secular:
            return 'Sacred'
        if not self.sacred_or_secular:
            return 'Secular'
        if self.sacred_or_secular is None:
            return 'Non Applicable'

    @property
    def symbolic_files(self):
        """Gets all the Symbolic Files related to this Work/Section/Part"""
        ids = []
        sources = self.sources.all()
        for source in sources:
            ids.extend(list(source.manifested_by_sym_files.values_list(
                    'id', flat=True)))
        files = SymbolicMusicFile.objects.filter(id__in=ids)
        return files

    def get_contributions(self):
        contributions = {
            'composers': self.composers,
            'authors':   self.authors
            }
        return contributions

    class Meta(CustomBaseModel.Meta):
        db_table = 'musical_work'
        verbose_name_plural = 'Musical Works'
