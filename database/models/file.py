from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.encoder import Encoder
from database.models.validator import Validator


class File(CustomBaseModel):
    """Base abstract model with fields common to all file types

    Most if not all fields should be extracted automatically
    """
    file_type = models.CharField(max_length=10)
    file_size = models.PositiveIntegerField()
    version = models.CharField(max_length=20, null=True)
    encoding_date = models.DateTimeField(null=True)
    encoded_with = models.ForeignKey(Encoder, on_delete=models.PROTECT,
                                     null=False)
    validated_by = models.ForeignKey(Validator, on_delete=models.SET_NULL,
                                     null=True, blank=True)

    class Meta(CustomBaseModel.Meta):
        abstract = True
