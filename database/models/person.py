"""Define a Person model"""
from django.apps import apps
from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.db.models import QuerySet

from database.models.custom_base_model import CustomBaseModel
from database.utils.model_utils import clean_date


class Person(CustomBaseModel):
    """A real world person that contributed to a MusicalWork/Section/Part
    
    Attributes
    ----------
    Person.given_name : models.CharField
        The given name of this Person
        
    Person.surname : models.CharField
        The surname of this Person
        
    Person.range_date_birth : django.contrib.postgres.fields.DateRangeField
        The possible range of dates of the birth of this Person
        If the date is know, then the beginning and end of range will be equal
    
    Person.range_date_death : django.contrib.postgres.fields.DateRangeField
        The possible range of dates of the death of this Person
        If the date is know, then the beginning and end of range will be equal
        
    Person.birth_location : models.ForeignKey
        Reference to the GeographicArea where this Person was born
        
    Person.death_location : models.ForeignKey
        Reference to the GeographicArea where this Person died
        
    Person.authority_control_url : models.URLField
        An URL linking to an authority control description of this Person

    Person.authority_control_key : models.IntegerField
        The identifier of this Person in the authority control

    Person.contributions : models.ManyToOneRel
        References to the Contributions made by this Person

    Person.published : models.ManyToOneRel
        References to the CollectionsOfSources published by this Person

    See Also
    --------
    database.models.CustomBaseModel
    database.models.GeographicArea
    database.models.Contribution
    database.models.CollectionOfSources
    """
    given_name = models.CharField(max_length=100,
                                  blank=False,
                                  help_text='The given name of this Person',
                                  default="")
    surname = models.CharField(max_length=100,
                               blank=True,
                               default="",
                               help_text='The surname of this Person, '
                                         'leave blank if it is unknown')
    range_date_birth = DateRangeField(null=True,
                                      blank=True,
                                      help_text='The birth year of this '
                                                'Person. The format is '
                                                'YYYY-MM-DD. '
                                                'If certain, put the '
                                                'beginning and end of the '
                                                'range as the same. If '
                                                'uncertain, enter a range '
                                                'that is generally accepted')
    range_date_death = DateRangeField(null=True,
                                      blank=True,
                                      help_text='The death year of this '
                                                'Person. The format is '
                                                'YYYY-MM-DD. '
                                                'If certain, put the '
                                                'beginning and end of the '
                                                'range as the same. If '
                                                'uncertain, enter a range '
                                                'that is generally accepted')
    birth_location = models.ForeignKey('GeographicArea',
                                       null=True,
                                       on_delete=models.SET_NULL,
                                       blank=True,
                                       related_name='birth_location_of',
                                       help_text='The birth location of this '
                                                 'Person. Choose the most '
                                                 'specific possible.')
    death_location = models.ForeignKey('GeographicArea',
                                       null=True,
                                       on_delete=models.SET_NULL,
                                       blank=True,
                                       related_name='death_location_of',
                                       help_text='The death location of this '
                                                 'Person. Choose the most '
                                                 'specific possible.')
    authority_control_url = models.URLField(blank=True,
                                            null=True,
                                            help_text='An URI linking to an '
                                                      'authority control '
                                                      'description of this '
                                                      'Person')
    authority_control_key = models.IntegerField(unique=True,
                                                blank=True,
                                                null=True,
                                                help_text='The identifier of '
                                                          'this Person '
                                                          'in the authority '
                                                          'control')

    class Meta(CustomBaseModel.Meta):
        db_table = 'person'

    def __str__(self):
        if self.surname and self.given_name:
            return "{0}, {1} {2}".format(self.surname, self.given_name,
                                         self._get_life_span())
        if self.given_name and not self.surname:
            return '{0} {1}'.format(self.given_name, self._get_life_span())
        if self.surname and not self.given_name:
            return '{0} {1}'.format(self.surname, self._get_life_span())

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
        musical_work_model = apps.get_model('database', 'musicalwork')
        ids = set()
        contributions = self._get_contributions_by_role(role)
        for contribution in contributions:
            ids.add(contribution.contributed_to_work_id)
        works = musical_work_model.objects.filter(id__in=ids)
        return works

    def _get_sections_by_role(self, role: str) -> QuerySet:
        section_model = apps.get_model('database', 'section')
        ids = set()
        contributions = self._get_contributions_by_role(role)
        for contribution in contributions:
            ids.add(contribution.contributed_to_work_id)
        sections = section_model.objects.filter(id__in=ids)
        return sections

    def _get_parts_by_role(self, role: str) -> QuerySet:
        part_model = apps.get_model('database', 'part')
        ids = set()
        contributions = self._get_contributions_by_role(role)
        for contribution in contributions:
            ids.add(contribution.contributed_to_work_id)
        parts = part_model.objects.filter(id__in=ids)
        return parts

    @property
    def name(self) -> str:
        """Get print friendly version of this Person's name"""
        return self.given_name + ' ' + self.surname

    @property
    def date_of_birth(self) -> str:
        """Get a print friendly version of range_date_birth"""
        return clean_date(self.range_date_birth)

    @property
    def date_of_death(self) -> str:
        """Get a print friendly version of range_date_death"""
        return clean_date(self.range_date_death)

    @property
    def works_composed(self) -> QuerySet:
        """Get the MusicalWorks composed by this Person"""
        return self._get_works_by_role('COMPOSER')

    @property
    def works_arranged(self) -> QuerySet:
        """Get the MusicalWorks arranged by this Person"""
        return self._get_works_by_role('ARRANGER')

    @property
    def works_authored(self) -> QuerySet:
        """Get the MusicalWorks authored by this Person"""
        return self._get_works_by_role('AUTHOR')

    @property
    def works_transcribed(self) -> QuerySet:
        """Get the MusicalWorks transcribed by this Person"""
        return self._get_works_by_role('TRANSCRIBER')

    @property
    def works_improvised(self) -> QuerySet:
        """Get the MusicalWorks improvised by this Person"""
        return self._get_works_by_role('IMPROVISER')

    @property
    def works_performed(self) -> QuerySet:
        """Get the MusicalWorks performed by this Person"""
        return self._get_works_by_role('PERFORMER')

    @property
    def sections_composed(self) -> QuerySet:
        """Get the Sections arranged by this Person"""
        return self._get_sections_by_role('COMPOSER')

    @property
    def sections_arranged(self) -> QuerySet:
        """Get the Sections arranged by this Person"""
        return self._get_sections_by_role('ARRANGER')

    @property
    def sections_authored(self) -> QuerySet:
        """Get the Sections authored by this Person"""
        return self._get_sections_by_role('AUTHOR')

    @property
    def sections_transcribed(self) -> QuerySet:
        """Get the Sections transcribed by this Person"""
        return self._get_sections_by_role('TRANSCRIBER')

    @property
    def sections_improvised(self) -> QuerySet:
        """Get the Sections improvised by this Person"""
        return self._get_sections_by_role('IMPROVISER')

    @property
    def sections_performed(self) -> QuerySet:
        """Get the Sections performed by this Person"""
        return self._get_sections_by_role('PERFORMER')

    @property
    def parts_composed(self) -> QuerySet:
        """Get the Parts composed by this Person"""
        return self._get_parts_by_role('COMPOSER')

    @property
    def parts_arranged(self) -> QuerySet:
        """Get the Parts arranged by this Person"""
        return self._get_parts_by_role('ARRANGER')

    @property
    def parts_authored(self) -> QuerySet:
        """Get the Parts authored by this Person"""
        return self._get_parts_by_role('AUTHOR')

    @property
    def parts_transcribed(self) -> QuerySet:
        """Get the Parts transcribed by this Person"""
        return self._get_parts_by_role('TRANSCRIBER')

    @property
    def parts_improvised(self) -> QuerySet:
        """Get the Parts improvised by this Person"""
        return self._get_parts_by_role('IMPROVISER')

    @property
    def parts_performed(self) -> QuerySet:
        """Get the Parts performed by this Person"""
        return self._get_parts_by_role('PERFORMER')
