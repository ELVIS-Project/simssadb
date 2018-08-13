from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Max, Min

from database.models.custom_base_model import CustomBaseModel
from database.models.feature_type import FeatureType
from database.models.software import Software
from database.models.symbolic_music_file import SymbolicMusicFile


class ExtractedFeatureManager(models.Manager):
    """A custom manager for ExtractedFeature"""

    def min_and_max(self, name):
        """Return the minimum and maximum values of a feature

        Parameters
        ----------
        name : str
            The name of the feature to get the minimum and maximum values

        Returns
        -------
        min_and_max : dict
            A dictionary containing the minimum and maximum values of the
            feature
        """
        features = self.get_queryset().exclude(value__len__gt=1).filter(
                name=name).only('value')
        min_and_max = features.aggregate(min_val=Min('value'), max_val=Max(
                'value'))
        return min_and_max


class ExtractedFeature(CustomBaseModel):
    """Content-based data extracted from a file"""
    instance_of_feature = models.ForeignKey(FeatureType,
                                            on_delete=models.PROTECT,
                                            null=False, blank=False,
                                            related_name='instances')
    value = ArrayField(models.FloatField(),
                       help_text='The value of the Extracted Feature. Encoded '
                                 'as an array but if the Extracted Feature is '
                                 'scalar it is an array of length = 1')
    extracted_with = models.ForeignKey(Software, on_delete=models.PROTECT,
                                       null=False, blank=False,
                                       help_text='The Software used to extract'
                                                 'this Extracted Feature')

    feature_of = models.ForeignKey(SymbolicMusicFile, on_delete=models.CASCADE,
                                   null=False, blank=False,
                                   related_name='extracted_features',
                                   help_text='The Symbolic File from which '
                                             'the feature was extracted')
    objects = ExtractedFeatureManager()

    def __str__(self):
        return "{0}".format(self.instance_of_feature.name)

    def save(self, *args, **kwargs):
        super(ExtractedFeature, self).save(*args, **kwargs)
        assert (len(self.value) == self.instance_of_feature.dimensions)
        self.instance_of_feature.max_and_min()

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

    @property
    def name(self):
        return self.instance_of_feature.name

    @property
    def is_histogram(self):
        if self.instance_of_feature.dimensions > 1 and len(self.value) > 1:
            return True
        else:
            return False

    @property
    def description(self):
        return self.instance_of_feature.description

    @property
    def code(self):
        return self.instance_of_feature.code
