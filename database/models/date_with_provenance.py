from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import DateRangeField


class DateWithProvenance(CustomBaseModel):

    date = DateRangeField()
    provenance = models.CharField(max_length=200, null=False, blank=True,
                                  help_text="This is where you enter where "
                                            "you got the information from")

    def __str__(self):
        return "{0}:{1}".format(self.date, self.provenance)

    class Meta(CustomBaseModel.Meta):
        db_table = 'date_with_provenance'
