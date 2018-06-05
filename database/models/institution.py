from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.geographic_area import GeographicArea


class Institution(CustomBaseModel):
    name = models.CharField(max_length=40, blank=False)
    located_at = models.ForeignKey(GeographicArea, on_delete=models.CASCADE)
    website = models.URLField()


    class Meta(CustomBaseModel.Meta):
        db_table = 'institution'
