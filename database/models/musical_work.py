from django.contrib.postgres.fields import ArrayField
from django.db import models

from database.mixins.contributed_to_info_mixin import ContributedToInfoMixin
from database.mixins.file_and_source_info import FileAndSourceInfoMixin
from database.models.custom_base_model import CustomBaseModel
from database.models.genre import Genre
from database.models.section import Section


class MusicalWork(FileAndSourceInfoMixin, ContributedToInfoMixin,
                  CustomBaseModel):
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

    def __str__(self):
        return "{0}".format(self.variant_titles[0])

    def __composers_for_summary(self):
        composers = self.composers
        if len(composers) > 1:
            return composers[0]['person'].__str__() + ' and others'
        else:
            return composers[0]['person'].__str__()

    def prepare_summary(self):
        summary = {'display': self.__str__(),
                   'url': self.get_absolute_url(),
                   'composer': self.__composers_for_summary(),
                   'date': self.dates_of_composition[0],
                   'sections': self.sections.count()
                   }
        return summary


    class Meta(CustomBaseModel.Meta):
        db_table = 'musical_work'
