from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Validator(CustomBaseModel):
    """A User or Software that verified the quality of a File or Source

    The relationship to User or Software is implemented using GenericForeignKey
    """
    work_flow = models.TextField()
    notes = models.TextField()

    limit = models.Q(app_label='database', model='software') | models.Q(
            app_label='database', model='user')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    is_a = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "{0} as validator".format(self.is_a)


    class Meta(CustomBaseModel.Meta):
        db_table = 'validator'
