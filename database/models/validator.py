from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Validator(CustomBaseModel):
    work_flow = models.TextField()
    notes = models.TextField()

    limit = models.Q(app_label='database', model='software') | \
            models.Q(app_label='database', model='user')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    is_a = GenericForeignKey('content_type', 'object_id')

    class Meta(CustomBaseModel.Meta):
        db_table = 'validator'
