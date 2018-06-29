from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import DateRangeField, ArrayField
from database.models.geographic_area import GeographicArea


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
                                                'Person. If certain, put the '
                                                'beginning and end of the '
                                                'range as the same. If '
                                                'uncertain, enter a range '
                                                'that is generally accepted')
    range_date_death = DateRangeField(null=True,
                                      help_text='The death year of this '
                                                'Person. If certain, put the '
                                                'beginning and end of the '
                                                'range as the same. If '
                                                'uncertain, enter a range '
                                                'that is generally accepted')
    birth_location = models.ForeignKey(GeographicArea, null=True,
                                       on_delete=models.SET_NULL, blank=True,
                                       related_name='birth_location_of',
                                       help_text='The birth location of this '
                                                 'Person. Choose the most '
                                                 'specific possible.')
    death_location = models.ForeignKey(GeographicArea, null=True,
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
    parts_contributed_to = models.ManyToManyField(
            'Part',
            through='ContributedTo',
            through_fields=('person', 'contributed_to_part'),
            help_text='The Parts that this Person contributed to'
    )
    sections_contributed_to = models.ManyToManyField(
            'Section',
            through='ContributedTo',
            through_fields=('person', 'contributed_to_section'),
            help_text='The Sections that this Person contributed to'
    )
    works_contributed_to = models.ManyToManyField(
            'MusicalWork',
            through='ContributedTo',
            through_fields=('person', 'contributed_to_work'),
            help_text='The Musical Works that this Person contributed to'
    )

    def __str__(self):
        return "{0} {1}".format(self.given_name, self.surname)


    class Meta(CustomBaseModel.Meta):
        db_table = 'person'
