from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.geographic_area import GeographicArea


class LocationWithProvenance(CustomBaseModel):

    location = models.ForeignKey(GeographicArea, on_delete=models.PROTECT)
    provenance = models.CharField(max_length=200, null=False, blank=True,
                                  help_text="This is where you enter where "
                                            "you got the information from")

    def __str__(self):
        return "{0}:{1}".format(self.location, self.provenance)

    class Meta(CustomBaseModel.Meta):
        db_table = 'location_with_provenance'
