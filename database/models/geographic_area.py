from django.db import models
from database.models.custom_base_model import CustomBaseModel


class GeographicArea(CustomBaseModel):
    """A geographic area that can be part of another area"""
    name = models.CharField(max_length=200)
    part_of = models.ForeignKey('self', on_delete=models.CASCADE)


    class Meta:
        db_table = 'geographic_area'
