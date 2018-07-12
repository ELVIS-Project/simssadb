from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.encoder import Encoder
from database.models.validator import Validator
from django.contrib.postgres.fields import JSONField


class File(CustomBaseModel):
    """Base abstract model with fields common to all file types

    Most if not all fields should be extracted automatically
    """
    file_type = models.CharField(max_length=10, help_text='The format of the '
                                                          'File')
    file_size = models.PositiveIntegerField(null=True, blank=True,
                                            help_text='The size of the File '
                                                      'in bytes')
    version = models.CharField(max_length=20, null=True,
                               help_text='The version of the encoding schema '
                                         '(i.e. MEI 2.0)')
    encoding_date = models.DateTimeField(null=True,
                                         help_text='The date the File was '
                                                   'encoded')
    encoded_with = models.ForeignKey(Encoder, on_delete=models.PROTECT,
                                     null=False, help_text='The Encoder of '
                                                           'this File')
    validated_by = models.ForeignKey(Validator, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     help_text='The Validator of this file')
    extra_metadata = JSONField(null=True, blank=True,
                               help_text='Any extra metadata associated with '
                                         'the File')

    def __prepare_summary(self):
        pass

    class Meta(CustomBaseModel.Meta):
        abstract = True
