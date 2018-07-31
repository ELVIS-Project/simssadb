from django.db import models

import database.mixins.contribution_helper as contribution_helper
from database.mixins.file_and_source_info import FileAndSourceInfoMixin
from database.models.custom_base_model import CustomBaseModel


class Section(FileAndSourceInfoMixin, CustomBaseModel):
    """
    A component of a Musical Work e.g. an Aria in an Opera

    Can alternatively be a Musical Work in its entirety.
    A purely abstract entity that can manifest in differing version.
    Can exist in more than one Musical Work.
    Divided into one or more parts.
    A Section can be divided into more Sections.
    Must have at least one part.
    """
    title = models.CharField(max_length=200,
                             help_text='The title of this Section')
    ordering = models.PositiveIntegerField(null=True, blank=True,
                                           help_text='A number representing '
                                                     'the order of this '
                                                     'Section within a Musical '
                                                     'Work')
    parent_sections = models.ManyToManyField('self',
                                             related_name='child_sections',
                                             blank=True,
                                             help_text='Sections that contain '
                                                       'this Section')
    contributors = models.ManyToManyField(
            'Person',
            through='ContributedTo',
            through_fields=('contributed_to_section', 'person'),
            help_text='All the People that '
                      'contributed to this '
                      'Musical Work in different '
                      'capacities such as '
                      'composer or arranger')

    @property
    def instrumentation(self):
        """Gets all the Instruments used in this Musical Work"""
        instruments = set()
        for part in self.parts.all():
            instruments.add(part.written_for)
        return instruments

    @staticmethod
    def _composers_for_summary(composers):
        if len(composers) > 1:
            return composers[0]['person'].__str__() + ' and others'
        else:
            return composers[0]['person'].__str__()

    @staticmethod
    def _works_for_summary(works):
        if works.count() > 1:
            return works[0].__str__() + ' and others'
        return works[0].__str__()

    def __str__(self):
        return "{0}".format(self.title)

    @staticmethod
    def _badge_name(parts_count):
        if parts_count > 1:
            return 'parts'
        else:
            return 'part'

    @property
    def certainty(self):
        """Returns True if all the relationships have certain == True"""
        certainties = self.contributed_to.values_list('certain', flat=True)
        if False in certainties:
            return False
        else:
            return True

    @property
    def composers(self):
        contributions = self.contributed_to.all().select_related('person')
        contributions_summaries = contribution_helper.get_contributions_summaries(
                contributions)
        return contribution_helper.filter_contributions_by_role(
                contributions_summaries, 'composer')

    @property
    def authors(self):
        contributions = self.contributed_to.all().select_related('person')
        contributions_summaries = contribution_helper.get_contributions_summaries(
                contributions)
        return contribution_helper.filter_contributions_by_role(
                contributions_summaries, 'author')

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

    def _prepare_summary(self):
        contributions = self.contributed_to.all().select_related('person')
        works = self.in_works.all()
        contributions_summaries = contribution_helper.get_contributions_summaries(
                contributions)
        composers = contribution_helper.filter_contributions_by_role(
                contributions_summaries, 'composer')
        parts_count = self.parts.count()

        if contribution_helper.dates_of_contribution(composers):
            date = contribution_helper.dates_of_contribution(composers)[0]
        else:
            date = 'Unknown'

        summary = {
            'display':      self.__str__(),
            'url':          self.get_absolute_url(),
            'composer':     self._composers_for_summary(composers),
            'date':         date,
            'badge_name':   self._badge_name(parts_count),
            'badge_count':  parts_count,
            'musical work': self._works_for_summary(works)
            }
        return summary

    def get_related(self):
        related = {
            'musical_works':   {
                'list':        self.in_works.all(),
                'model_name':  'Part of Musical Works',
                'model_count': self.in_works.count(),
                },
            'sym_files':       {
                'list':        self.symbolic_files,
                'model_name':  'Symbolic Music Files',
                'model_count': len(self.symbolic_files)
                },
            'parent_sections': {
                'list':        self.parent_sections.all(),
                'model_name':  'Parent Sections',
                'model_count': self.parent_sections.count()
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
            'title':         self.__str__(),
            'ordering':      self.ordering,
            'contributions': self.get_contributions(),
            'source':        list(self.collections_of_sources),
            'languages':     list(self.languages),
            'related':       self.get_related()
            }
        return detail_dict

    class Meta(CustomBaseModel.Meta):
        db_table = 'section'
