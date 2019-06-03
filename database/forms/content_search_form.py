from django import forms
from database.models import ExtractedFeature
from django.db.models import Max, Min
from database.widgets.range_slider import RangeSlider

ROUND_OFF_VALUE = 3


class CharFieldWithGroup(forms.CharField):

    def __init__(self, group, *args, **kwargs):
        super(CharFieldWithGroup, self).__init__(*args, **kwargs)
        self.group = group


class ContentSearchForm(forms.Form):
    def __init__(self, feature_types, file_ids=None, *args, **kwargs):
        super(ContentSearchForm, self).__init__(*args, **kwargs)
        feature_types = (list(feature_types))

        for feature in feature_types:
            if feature.min_val == feature.max_val:
                continue
            name = feature.name
            code = feature.code
            group = feature.group
            min_val = feature.min_val
            max_val = feature.max_val
            help_text = feature.description
            attrs = {
                'disabled': 'true',
                'name':     name,
                'code':     code,
                'min':      min_val,
                'max':      max_val,
                'values':   [min_val, max_val]
                }
            if code in self.data:
                new_min_val, new_max_val = self.data[code].split(',')
                attrs['disabled'] = 'false'
                attrs['values'] = [float(new_min_val), float(new_max_val)]
            widget = RangeSlider(attrs=attrs)
            self.fields[name] = CharFieldWithGroup(widget=widget,
                                                   required=False,
                                                   group=group,
                                                   help_text=help_text)
