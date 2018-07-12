from cached_property import cached_property
from database.models.encoder_validator_base_model import \
    EncoderValidatorBaseModel


class Encoder(EncoderValidatorBaseModel):
    """A User or Software that encoded a file using a workflow"""

    def __str__(self):
        if self.user_id is not None:
            return "{0} as encoder".format(self.user)
        if self.software_id is not None:
            return "{0} as encoder".format(self.software)
        raise AssertionError('Neither User or Software is set')

    def prepare_summary(self):
        summary = {'display': self.__str__(),
                   'url': self.get_absolute_url()}
        return summary

    class Meta(EncoderValidatorBaseModel.Meta):
        db_table = 'encoder'
