from database.models.encoder_validator_base_model import \
    EncoderValidatorBaseModel


class Encoder(EncoderValidatorBaseModel):
    """A User or Software that encoded a file using a workflow"""

    def __str__(self):
        if self.user_id is not None:
            return "{0} (Encoder)".format(self.user)
        if self.software_id is not None:
            return "{0}".format(self.software)
        raise AssertionError('Neither User or Software is set')

    def _prepare_summary(self):
        summary = {'display': self.__str__(),
                   'url': self.get_absolute_url()}
        return summary

    def get_related(self):
        related = {
            'sym_files': {'list': self.symbolicmusicfile_set.all(),
                          'model_name': 'Symbolic Music Files Encoded',
                          'model_count': self.symbolicmusicfile_set.count()
                          }
        }

        return related

    def detail(self):
        detail_dict = {
            'title': self.__str__(),
            'workflow': self.work_flow_text,
            'notes': self.notes,
            'related': self.get_related(),
        }

        return detail_dict


    class Meta(EncoderValidatorBaseModel.Meta):
        db_table = 'encoder'
