from django import forms
from django.db.models import Max, Min

from database.models.extracted_feature import ExtractedFeature


class ContentSearchForm(forms.Form):

    @staticmethod
    def get_all_feature_names():
        extracted_features = ExtractedFeature.objects.all().filter(
            name='Total Number of Notes')
        names = set()
        for feature in extracted_features:
            if not len(feature.value) > 1:
                names.add(feature.name)
        return names

    @staticmethod
    def get_min_max(feature_name):
        features = ExtractedFeature.objects.all().filter(name=feature_name)
        max_val = features.aggregate(Max('value'))
        min_val = features.aggregate(Min('value'))

        return min_val['value__min'][0], max_val['value__max'][0]

    @staticmethod
    def make_attrs_dict(min_max):
        min_val = round(min_max[0], 3)
        max_val = round(min_max[1], 3)

        attrs_dict = {
            'data-provide':        'slider',
            'data-slider-min':     min_val,
            'data-slider-max':     max_val,
            'data-slider-step':    0.001,
            'data-slider-range':   'true',
            'data-slider-value':   [min_val, max_val],
            'data-slider-enabled': 'true'
            }
        return attrs_dict

    def search(self, name, min_val, max_val):
        features = ExtractedFeature.objects.all().filter(name=name)
        features = features.filter(value__0__gte=min_val)
        features = features.filter(value__0__lte=max_val).prefetch_related(
                'feature_of')
        files = []
        for feature in features:
            files.append(feature.feature_of)
        return files

    def __init__(self, *args, **kwargs):
        super(ContentSearchForm, self).__init__(*args, **kwargs)
        names = list(self.get_all_feature_names())
        for name in names:
            print(name)
            attrs_dict = self.make_attrs_dict(self.get_min_max(name))
            widget = forms.TextInput(attrs=attrs_dict)
            self.fields[name] = forms.CharField(widget=widget, required=False)
