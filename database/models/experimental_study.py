from django.db import models
from database.models.custom_base_model import CustomBaseModel


class ExperimentalStudy(CustomBaseModel):
    title = models.CharField(max_length=200, blank=False)
    published = models.BooleanField(default=False)
    date_published = models.DateField(null=True)
    link = models.URLField(blank=True)


    class Meta(CustomBaseModel.Meta):
        db_table = 'experimental_study'
