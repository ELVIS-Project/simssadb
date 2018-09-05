from django.db import models

import database.mixins.contribution_helper as contribution_helper
from database.mixins.file_and_source_info import FileAndSourceInfoMixin
from database.models.custom_base_model import CustomBaseModel
from database.models.instrument import Instrument

# TODO: improve handling of related data for child/parent relationships


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
                                                       'this Section',
                                             symmetrical=False)
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
        """Gets all the Instruments used in this Section"""
        instruments = Instrument.objects.none()
        for part in self.parts.all():
            instruments = instruments.union(Instrument.objects.filter(
                    pk=part.written_for.id))
        if not instruments and self.parent_sections.exists():
            for parent in self.parent_sections.all():
                instruments = instruments.union(parent.instrumentation)
        if not instruments and self.child_sections.exists():
            for child in self.child_sections.all():
                instruments = instruments.union(child.instrumentation)
        return instruments

    def __str__(self):
        return "{0}".format(self.title)

    @property
    def certainty_of_attribution(self):
        """Returns True if all the relationships have certain == True"""
        certainties = self.contributed_to.values_list('certain', flat=True)
        if False in certainties:
            return False
        else:
            return True

    @property
    def composers(self):
        contributions = self.contributed_to.all().select_related('person')
        if not contributions.exists() and self.parent_sections.exists():
            contributions = self.parent_sections.all()[0].contributed_to.all(
                    ).select_related('person')
        contributions_summaries = contribution_helper.\
            get_contributions_summaries(contributions)
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

    def get_contributions(self):
        contributions = {
            'composers': self.composers,
            'authors':   self.authors
            }
        return contributions

    class Meta(CustomBaseModel.Meta):
        db_table = 'section'
