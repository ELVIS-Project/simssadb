from django.db import models
from database.models.custom_base_model import CustomBaseModel


class GeographicArea(CustomBaseModel):
    """A geographic area that can be part of another area"""
    name = models.CharField(max_length=200)
    part_of = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
                                blank=True)
    authority_control_url = models.URLField(null=True, blank=True)
    authority_control_key = models.IntegerField(unique=True, blank=True,
                                                null=True)

    def __str__(self):
        return "{0}".format(self.name)


    class Meta:
        db_table = 'geographic_area'
