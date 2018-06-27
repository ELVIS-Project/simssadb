from django.db import models
from database.models.encoder_validator_base_model import \
    EncoderValidatorBaseModel
from database.models.source import Source


class Validator(EncoderValidatorBaseModel):
    """
    A User or Software that verified the quality of Files against Sources.

    The user or software must use a workflow
    """

    sources = models.ManyToManyField(Source, blank=False,
                                     related_name='validated_by')

    def __str__(self):
        if self.user_id is not None:
            return "{0} as validator".format(self.user)
        if self.software_id is not None:
            return "{0} as validator".format(self.software)
        raise AssertionError('Neither User or Software is set')

    class Meta(EncoderValidatorBaseModel.Meta):
        db_table = 'validator'
