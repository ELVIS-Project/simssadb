from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import DateRangeField, ArrayField
from database.models.geographic_area import GeographicArea


class Person(CustomBaseModel):
    """Represents a real world person that contributed to a musical work"""
    names = ArrayField(models.CharField(max_length=100, blank=True),
                      blank=False, null=False)
    range_date_birth = DateRangeField(null=True)
    range_date_death = DateRangeField(null=True)
    birth_location = models.ForeignKey(GeographicArea, null=True,
                                       on_delete=models.SET_NULL, blank=True,
                                       related_name='birth_location_of')
    death_location = models.ForeignKey(GeographicArea, null=True,
                                       on_delete=models.SET_NULL, blank=True,
                                       related_name='death_location_of')
    viaf_url = models.URLField(null=True, blank=True)
    other_authority_control_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return "{0}".format(self.names[0])


    class Meta(CustomBaseModel.Meta):
        db_table = 'person'
