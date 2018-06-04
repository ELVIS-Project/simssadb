from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import ArrayField


class MusicalWork(CustomBaseModel):
    title = models.CharField(max_length=200, blank=False)
    alternative_titles = ArrayField(
            ArrayField(
                    models.CharField(max_length=200, blank=True)
            )
    )
    subtitle = models.CharField(max_length=200, blank=True)
    opus = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta(CustomBaseModel.Meta):
        db_table = 'musical_work'
