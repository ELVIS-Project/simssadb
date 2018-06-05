from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from database.models.source import Source


class MusicalInstance(CustomBaseModel):
    title = models.CharField(max_length=200)

    limit = models.Q(app_label='database', model='musical_work') | \
            models.Q(app_label='database', model='section') | \
            models.Q(app_label='database', model='part')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    instance_of = GenericForeignKey('content_type', 'object_id')
    source = models.OneToOneField(Source, on_delete=models.CASCADE)

    class Meta(CustomBaseModel.Meta):
        db_table = 'musical_instance'
