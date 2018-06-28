from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import DateRangeField, ArrayField
from database.models.geographic_area import GeographicArea


class Person(CustomBaseModel):
    """Represents a real world person that contributed to a musical work"""
    given_name = models.CharField(max_length=100, null=False, blank=False, default="")
    surname = models.CharField(max_length=100, null=False, blank=True,
                               default="")
    range_date_birth = DateRangeField(null=True)
    range_date_death = DateRangeField(null=True)
    birth_location = models.ForeignKey(GeographicArea, null=True,
                                       on_delete=models.SET_NULL, blank=True,
                                       related_name='birth_location_of')
    death_location = models.ForeignKey(GeographicArea, null=True,
                                       on_delete=models.SET_NULL, blank=True,
                                       related_name='death_location_of')
    authority_control_url = models.URLField(null=True, blank=True)
    authority_control_key = models.IntegerField(unique=True, blank=True,
                                                null=True)
    parts_contributed_to = models.ManyToManyField(
            'Part',
            through='ContributedTo',
            through_fields=('person', 'contributed_to_part')
    )
    sections_contributed_to = models.ManyToManyField(
            'Section',
            through='ContributedTo',
            through_fields=('person', 'contributed_to_section')
    )
    works_contributed_to = models.ManyToManyField(
            'MusicalWork',
            through='ContributedTo',
            through_fields=('person', 'contributed_to_work')
    )
    def __str__(self):
        return "{0} {1}".format(self.given_name, self.surname)


    class Meta(CustomBaseModel.Meta):
        db_table = 'person'
