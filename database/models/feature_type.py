from django.db import models
from django.db.models import Max, Min

from database.models.custom_base_model import CustomBaseModel


class FeatureType(CustomBaseModel):
    name = models.CharField(max_length=200, blank=False, null=False,
                            help_text='The name of the Extracted FeatureType')
    code = models.CharField(max_length=5, blank=False, null=False,
                            help_text='The jSymbolic code of the Extracted '
                                      'FeatureType')
    description = models.TextField(blank=True, null=True,
                                   help_text='A description of the Extracted '
                                             'FeatureType')

    is_sequential = models.NullBooleanField(blank=True, null=True,
                                            help_text='whether a feature can '
                                                      'be extracted from '
                                                      'sequential windows of a '
                                                      'data instance (e.g. '
                                                      'individual measures, '
                                                      'sections, etc.); a '
                                                      'value of true means '
                                                      'that it can, a value of '
                                                      'false means that only '
                                                      'one feature value may '
                                                      'be extracted per '
                                                      'instance (i.e. per '
                                                      'symbolic feature file)')

    dimensions = models.PositiveIntegerField(help_text='The number of '
                                                       'dimensions of the '
                                                       'Extracted FeatureType')

    min_val = models.FloatField(help_text='The minimum value of this '
                                          'Extracted FeatureType across all files '
                                          'that have this feature')

    max_val = models.FloatField(help_text='The maximum value of this '
                                          'Extracted FeatureType across all files '
                                          'that have this feature')

    def max_and_min(self):
        if self.dimensions == 1:
            self.max_val = self.instances.all().aggregate(max_val=Max('value'))[
                'max_val'][0]
            self.min_val = self.instances.all().aggregate(min_val=Min('value'))[
                'min_val'][0]
            self.save()

    class Meta(CustomBaseModel.Meta):
        db_table = 'feature'
