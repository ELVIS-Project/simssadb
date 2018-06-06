from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import DateRangeField
from database.models.institution import Institution


class Person(CustomBaseModel):
    name = models.CharField(max_length=100, blank=False)
    range_date_birth = DateRangeField()
    range_date_death = DateRangeField()
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL,
                                    null=True)

    class Meta(CustomBaseModel.Meta):
        db_table = 'person'
