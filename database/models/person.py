from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import DateRangeField
from database.models.institution import Institution
from gm2m import GM2MField


class Person(CustomBaseModel):
    """Represents a real world person that contributed to a musical work"""
    name = models.CharField(max_length=100, blank=False)
    range_date_birth = DateRangeField(null=True)
    range_date_death = DateRangeField(null=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL,
                                    null=True)

    contributed_to = GM2MField(through='ContributedTo')

    class Meta(CustomBaseModel.Meta):
        db_table = 'person'
