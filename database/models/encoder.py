from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Encoder(CustomBaseModel):
    """A User or Software that encoded a File from a Source

    The relationship to user or software is implemented using GenericForeignKey
    """
    work_flow = models.TextField()
    notes = models.TextField()

    # GenericForeignKey to allow polymorphic relationship to software and user
    limit = models.Q(app_label='database', model='software') | models.Q(
            app_label='database', model='user')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    is_a = GenericForeignKey('content_type', 'object_id')

    class Meta(CustomBaseModel.Meta):
        db_table = 'encoder'
