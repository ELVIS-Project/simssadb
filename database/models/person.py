from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.db.models import QuerySet
from django.apps import apps

from database.models.custom_base_model import CustomBaseModel
from database.utils.model_utils import clean_date


class Person(CustomBaseModel):
    """Represents a real world person that contributed to a musical work"""
    given_name = models.CharField(max_length=100, null=False, blank=False,
                                  help_text='The given name of this Person',
                                  default="")
    surname = models.CharField(max_length=100, null=False, blank=True,
                               default="",
                               help_text='The surname of this Person, '
                                         'leave blank if it is unknown')
    range_date_birth = DateRangeField(null=True,
                                      help_text='The birth year of this '
                                                'Person. The format is '
                                                'YYYY-MM-DD. '
                                                'If certain, put the '
                                                'beginning and end of the '
                                                'range as the same. If '
                                                'uncertain, enter a range '
                                                'that is generally accepted')
    range_date_death = DateRangeField(null=True,
                                      help_text='The death year of this '
                                                'Person. The format is '
                                                'YYYY-MM-DD. '
                                                'If certain, put the '
                                                'beginning and end of the '
                                                'range as the same. If '
                                                'uncertain, enter a range '
                                                'that is generally accepted')
    birth_location = models.ForeignKey('GeographicArea', null=True,
                                       on_delete=models.SET_NULL, blank=True,
                                       related_name='birth_location_of',
                                       help_text='The birth location of this '
                                                 'Person. Choose the most '
                                                 'specific possible.')
    death_location = models.ForeignKey('GeographicArea', null=True,
                                       on_delete=models.SET_NULL, blank=True,
                                       related_name='death_location_of',
                                       help_text='The death location of this '
                                                 'Person. Choose the most '
                                                 'specific possible.')
    authority_control_url = models.URLField(null=True, blank=True,
                                            help_text='An URI linking to an '
                                                      'authority control '
                                                      'description of this '
                                                      'Person')
    authority_control_key = models.IntegerField(unique=True, blank=True,
                                                null=True,
                                                help_text='The identifier of '
                                                          'this Person '
                                                          'in the authority '
                                                          'control')

    class Meta(CustomBaseModel.Meta):
        db_table = 'person'

    def __str__(self):
        if self.surname and self.given_name:
            return "{0}, {1} ({2})".format(self.surname, self.given_name,
                                           self._get_life_span())
        if self.given_name and not self.surname:
            return '{0} ({1})'.format(self.given_name, self._get_life_span())
        if self.surname and not self.given_name:
            return '{0} ({1})'.format(self.surname, self._get_life_span())

    def _get_life_span(self) -> str:
        if self.range_date_birth and self.range_date_death:
            return clean_date(self.range_date_birth) \
                   + '--' + \
                   clean_date(self.range_date_death)
        else:
            return ""

    def _get_contributions_by_role(self, role: str) -> QuerySet:
        return self.contributions.filter(role=role)

    def _get_works_by_role(self, role: str) -> QuerySet:
        musical_work_model = apps.get_model('database', 'musical_work')
        ids = []
        contributions = self._get_contributions_by_role(role)
        for contribution in contributions:
            ids.append(contribution.contributed_to_work_id)
        works = musical_work_model.objects.filter(id__in=ids)
        return works

    def _get_sections_by_role(self, role: str) -> QuerySet:
        section_model = apps.get_model('database', 'section')
        ids = []
        contributions = self._get_contributions_by_role(role)
        for contribution in contributions:
            ids.append(contribution.contributed_to_work_id)
        sections = section_model.objects.filter(id__in=ids)
        return sections

    def _get_parts_by_role(self, role: str) -> QuerySet:
        part_model = apps.get_model('database', 'part')
        ids = []
        contributions = self._get_contributions_by_role(role)
        for contribution in contributions:
            ids.append(contribution.contributed_to_work_id)
        parts = part_model.objects.filter(id__in=ids)
        return parts

    @property
    def name(self) -> str:
        return self.given_name + ' ' + self.surname

    @property
    def works_composed(self) -> QuerySet:
        return self._get_works_by_role('COMPOSER')

    @property
    def works_arranged(self) -> QuerySet:
        return self._get_works_by_role('ARRANGER')

    @property
    def works_authored(self) -> QuerySet:
        return self._get_works_by_role('AUTHOR')

    @property
    def works_transcribed(self) -> QuerySet:
        return self._get_works_by_role('TRANSCRIBER')

    @property
    def works_improvised(self) -> QuerySet:
        return self._get_works_by_role('IMPROVISER')

    @property
    def works_performed(self) -> QuerySet:
        return self._get_works_by_role('PERFORMER')

    @property
    def sections_composed(self) -> QuerySet:
        return self._get_sections_by_role('COMPOSER')

    @property
    def sections_arranged(self) -> QuerySet:
        return self._get_sections_by_role('ARRANGER')

    @property
    def sections_authored(self) -> QuerySet:
        return self._get_sections_by_role('AUTHOR')

    @property
    def sections_transcribed(self) -> QuerySet:
        return self._get_sections_by_role('TRANSCRIBER')

    @property
    def sections_improvised(self) -> QuerySet:
        return self._get_sections_by_role('IMPROVISER')

    @property
    def sections_performed(self) -> QuerySet:
        return self._get_sections_by_role('PERFORMER')

    @property
    def parts_composed(self) -> QuerySet:
        return self._get_parts_by_role('COMPOSER')

    @property
    def parts_arranged(self) -> QuerySet:
        return self._get_parts_by_role('ARRANGER')

    @property
    def parts_authored(self) -> QuerySet:
        return self._get_parts_by_role('AUTHOR')

    @property
    def parts_transcribed(self) -> QuerySet:
        return self._get_parts_by_role('TRANSCRIBER')

    @property
    def parts_improvised(self) -> QuerySet:
        return self._get_parts_by_role('IMPROVISER')

    @property
    def parts_performed(self) -> QuerySet:
        return self._get_parts_by_role('PERFORMER')
