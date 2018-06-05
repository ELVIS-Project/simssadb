from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import ArrayField


class ExtractedFeature(CustomBaseModel):
    name = models.CharField(max_length=200, blank=False)
    value = ArrayField(
            ArrayField(
                    models.IntegerField()
            )
    )


    class Meta(CustomBaseModel.Meta):
        db_table = 'extracted_feature'
