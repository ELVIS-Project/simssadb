from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from database.models.software import Software


class ExtractedFeature(CustomBaseModel):
    name = models.CharField(max_length=200, blank=False)
    value = ArrayField(
            ArrayField(
                    models.IntegerField()
            )
    )

    limit = models.Q(app_label='database', model='symbolic_music_file') | \
            models.Q(app_label='database', model='audio_file') | \
            models.Q(app_label='database', model='image_file')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    feature_of = GenericForeignKey('content_type', 'object_id')
    extracted_with = models.ForeignKey(Software, on_delete=models.PROTECT, null=False, blank=False)


    class Meta(CustomBaseModel.Meta):
        db_table = 'extracted_feature'
