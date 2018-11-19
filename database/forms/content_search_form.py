from django import forms
from database.widgets.range_slider import RangeSlider

ROUND_OFF_VALUE = 3


class CharFieldWithGroup(forms.CharField):

    def __init__(self, group, *args, **kwargs):
        super(CharFieldWithGroup, self).__init__(*args, **kwargs)
        self.group = group


class ContentSearchForm(forms.Form):
    def __init__(self, feature_types, *args, **kwargs):
        super(ContentSearchForm, self).__init__(*args, **kwargs)
        feature_types = (list(feature_types))

        for feature in feature_types:
            if feature.min_val == feature.max_val:
                continue
            name = feature.name
            group = feature.group
            min_val = feature.min_val
            max_val = feature.max_val
            attrs = {
                'disabled': 'true',
                'name': name,
                'min': min_val,
                'max': max_val
                }
            if name in self.data:
                new_min_val, new_max_val = self.data[name].split(',')
                attrs['disabled'] = 'false',
                attrs['min'] = float(new_min_val)
                attrs['max'] = float(new_max_val)
            widget = RangeSlider(attrs=attrs)
            self.fields[name] = CharFieldWithGroup(widget=widget,
                                                   required=False,
                                                   group=group)
