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
                                     related_name='validated_by',
                                     help_text='The Sources validated by this '
                                               'validator')

    def __str__(self):
        if self.user_id is not None:
            return "{0} as validator".format(self.user)
        if self.software_id is not None:
            return "{0} as validator".format(self.software)
        raise AssertionError('Neither User or Software is set')

    def _prepare_summary(self):
        summary = {
            'display': self.__str__(),
            'url':     self.get_absolute_url()
            }
        return summary

    def get_related(self):
        related = {
            'sym_files': {
                'list':        self.symbolicmusicfile_set.all(),
                'model_name':  'Symbolic Music Files Validated',
                'model_count': self.symbolicmusicfile_set.count()
                },
            'sources':   {
                'list':        self.sources.all(),
                'model_name':  'Source Items Validated',
                'model_count': self.sources.count()
                }
            }

        return related

    def detail(self):
        detail_dict = {
            'title':    self.__str__(),
            'workflow': self.work_flow_text,
            'notes':    self.notes,
            'related':  self.get_related(),
            }

        return detail_dict

    class Meta(EncoderValidatorBaseModel.Meta):
        db_table = 'validator'
