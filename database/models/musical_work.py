from django.contrib.postgres.fields import ArrayField
from django.db import models

import database.mixins.contribution_helper as contribution_helper
from database.mixins.file_and_source_info import FileAndSourceInfoMixin
from database.models.custom_base_model import CustomBaseModel
from database.models.genre import Genre
from database.models.section import Section


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
                      'Musical Work. Include the opus number '
                      'if there is one')

    genres_as_in_style = models.ManyToManyField(Genre,
                                                related_name='style',
                                                help_text='The styles '
                                                          'attributed to this '
                                                          'Musical Work, '
                                                          'i.e. Classical, '
                                                          'Pop, Folk')
    genres_as_in_type = models.ManyToManyField(Genre,
                                               related_name='type',
                                               help_text='The type of work, '
                                                         'i.e. Sonata, Motet, '
                                                         '12-bar Blues')

    sections = models.ManyToManyField(Section, related_name='in_works',
                                      help_text='The Sections that this work '
                                                'contains. If the Musical '
                                                'Work is not formally divided '
                                                'into Sections, then it has '
                                                'one Section.')
    religiosity = models.NullBooleanField(null=True, blank=True, default=None,
                                          help_text='Whether the Musical Work is'
                                                    ' secular or religious. '
                                                    'Leave this blank if non '
                                                    'applicable.')
    authority_control_url = models.URLField(null=True, blank=True,
                                            help_text='An URI linking to an '
                                                      'authority control '
                                                      'description of this '
                                                      'Musical Work')
    authority_control_key = models.IntegerField(unique=True, blank=True,
                                                null=True,
                                                help_text='The identifier of '
                                                          'this Musical Work '
                                                          'in the authority '
                                                          'control')
    contributors = models.ManyToManyField(
            'Person',
            through='ContributedTo',
            through_fields=(
                'contributed_to_work', 'person'),
            help_text='All the People that '
                      'contributed to this '
                      'Musical Work in different '
                      'capacities such as '
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
        instruments = set()
        for section in self.sections.all():
            instruments.update(section.instrumentation)
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
        """Gets the date of contribution of all the composers of this Work/Section/Part"""
        dates = []
        relationships = self.contributed_to.filter(role='COMPOSER')
        for relationship in relationships:
            dates.append(relationship.date)
        return dates

    @property
    def places_of_composition(self):
        """Gets the place of contribution of all the composers of this Work/Section/Part"""
        places = []
        relationships = self.contributed_to.filter(role='COMPOSER')
        for relationship in relationships:
            places.append(relationship.location)
        return places

    def __str__(self):
        return "{0}".format(self.variant_titles[0])

    @staticmethod
    def _composers_for_summary(composers):
        if len(composers) > 1:
            return composers[0]['person'].__str__() + ' and others'
        else:
            return composers[0]['person'].__str__()

    def _badge_name(self):
        if self.sections.count() > 1:
            return 'sections'
        else:
            return 'section'

    @property
    def composers(self):
        contributions = self.contributed_to.all().select_related('person')
        contributions_summaries = \
            contribution_helper.get_contributions_summaries(contributions)
        return contribution_helper.filter_contributions_by_role(
                contributions_summaries, 'composer')

    @property
    def authors(self):
        contributions = self.contributed_to.all().select_related('person')
        contributions_summaries = \
            contribution_helper.get_contributions_summaries(contributions)
        return contribution_helper.filter_contributions_by_role(
                contributions_summaries, 'author')

    def _prepare_summary(self):
        contributions = self.contributed_to.all().select_related('person')
        contributions_summaries = contribution_helper.get_contributions_summaries(
                contributions)
        composers = contribution_helper.filter_contributions_by_role(
                contributions_summaries, 'composer')

        if contribution_helper.dates_of_contribution(composers):
            date = contribution_helper.dates_of_contribution(composers)[0]
        else:
            date = 'Unknown'

        summary = {
            'display':     self.__str__(),
            'url':         self.get_absolute_url(),
            'composer':    self._composers_for_summary(composers),
            'date':        date,
            'badge_name':  self._badge_name(),
            'badge_count': self.sections.count()
            }
        return summary

    @property
    def get_religiosity(self):
        if self.religiosity:
            return 'Sacred'
        if not self.religiosity:
            return 'Secular'
        if self.religiosity is None:
            return 'Non Applicable'

    def get_related(self):
        related = {
            'sections':  {
                'list':        self.sections.all(),
                'model_name':  'Sections',
                'model_count': self.sections.count()
                },
            'sym_files': {
                'list':        self.symbolic_files,
                'model_name':  'Symbolic Music Files',
                'model_count': len(self.symbolic_files)
                }
            }
        return related

    def get_contributions(self):
        contributions = {
            'composers': self.composers,
            'authors':   self.authors
            }
        return contributions

    def detail(self):
        detail_dict = {
            'title':                 self.variant_titles[0],
            'contributions':         self.get_contributions(),
            'variant_titles':        self.variant_titles[1:],
            'sacred/secular':        self.get_religiosity,
            'genre_(style)':         list(self.genres_as_in_style.all()),
            'genre_(type)':          list(self.genres_as_in_type.all()),
            'authority_control_url': self.authority_control_url,
            'source':                list(self.collections_of_sources),
            'languages':             list(self.languages),
            'related':               self.get_related()
            }
        return detail_dict

    class Meta(CustomBaseModel.Meta):
        db_table = 'musical_work'
        verbose_name_plural = 'Musical Works'
