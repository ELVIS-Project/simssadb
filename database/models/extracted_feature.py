from django.contrib.postgres.fields import ArrayField
from django.db import models

from database.models.custom_base_model import CustomBaseModel
from database.models.software import Software
from database.models.symbolic_music_file import SymbolicMusicFile


class ExtractedFeature(CustomBaseModel):
    """Content-based data extracted from a file"""
    name = models.CharField(max_length=200, blank=False,
                            help_text='The name of the Extracted Feature', default='')
    value = ArrayField(models.FloatField(),
                       help_text='The value of the Feature. Encoded as an '
                                 'array but if the Feature is scalar it '
                                 'is an array of length = 1')
    extracted_with = models.ForeignKey(Software, on_delete=models.PROTECT,
                                       null=False, blank=False,
                                       help_text='The Software used to extract'
                                                 'this Feature')

    feature_of = models.ForeignKey(SymbolicMusicFile, on_delete=models.CASCADE,
                                   null=False, blank=False,
                                   related_name='extracted_features',
                                   help_text='The Symbolic File from which '
                                             'the feature was extracted')

    def __str__(self):
        return "{0}".format(self.name)

    def _prepare_summary(self):
        summary = {
            'display': "{0}: {1}".format(self.name, self.value[0]),
            'url':     self.get_absolute_url(),
            }
        return summary

    def detail(self):
        detail_dict = {
            'title':          self.name,
            'value':          self.value,
            'extracted_with': self.extracted_with,
            'feature_of':     self.feature_of
            }

        return detail_dict

    class Meta(CustomBaseModel.Meta):
        db_table = 'extracted_feature'
