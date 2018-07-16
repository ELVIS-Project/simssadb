from django.db import models

from database.mixins.contributed_to_info_mixin import ContributedToInfoMixin
from database.mixins.file_and_source_info import FileAndSourceInfoMixin
from database.models.custom_base_model import CustomBaseModel


class Section(FileAndSourceInfoMixin, ContributedToInfoMixin, CustomBaseModel):
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

    def __composers_for_summary(self):
        composers = self.composers
        if len(composers) > 1:
            return composers[0]['person'].__str__() + ' and others'
        else:
            return composers[0]['person'].__str__()

    def __works_for_summary(self):
        work_count = self.in_works.count()
        if work_count > 1:
            return self.in_works.all()[0].__str__() + " and others"
        else:
            return self.in_works.all()[0].__str__()

    def __str__(self):
        return "{0}".format(self.title)

    def __badge_name(self):
        if self.parts.count() > 1:
            return 'parts'
        else:
            return 'part'

    def prepare_summary(self):
        summary = {'display': self.__str__(),
                   'url': self.get_absolute_url(),
                   'composer': self.__composers_for_summary(),
                   'date': self.dates_of_composition[0],
                   'badge_name': self.__badge_name(),
                   'badge_count': self.parts.count(),
                   'musical work': self.__works_for_summary()
                   }
        return summary

    class Meta(CustomBaseModel.Meta):
        db_table = 'section'
