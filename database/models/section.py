from django.db import models
from database.mixins.file_and_source_info import FileAndSourceInfoMixin
from database.models.custom_base_model import CustomBaseModel
import database.mixins.contribution_helper as contribution_helper


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
        print(certainties)
        if False in certainties:
            return False
        else:
            return True

    def prepare_summary(self):
        contributions = self.contributed_to.all().select_related('person')
        works = self.in_works.all()
        contributions_summaries = contribution_helper.get_contributions_summaries(contributions)
        composers = contribution_helper.filter_contributions_by_role(contributions_summaries, 'composer')
        parts_count = self.parts.count()

        if contribution_helper.dates_of_contribution(composers):
            date = contribution_helper.dates_of_contribution(composers)[0]
        else:
            date = 'Unknown'

        summary = {'display': self.__str__(),
                   'url': self.get_absolute_url(),
                   'composer': self._composers_for_summary(composers),
                   'date': date,
                   'badge_name': self._badge_name(parts_count),
                   'badge_count': parts_count,
                   'musical work': self._works_for_summary(works)
                   }
        return summary

    class Meta(CustomBaseModel.Meta):
        db_table = 'section'
