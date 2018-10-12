from django import forms

ROUND_OFF_VALUE = 3
STEP_VALUE = 0.001


class CharFieldWithGroup(forms.CharField):

    def __init__(self, group, *args, **kwargs):
        super(CharFieldWithGroup, self).__init__(*args, **kwargs)
        self.group = group


class ContentSearchForm(forms.Form):

    @staticmethod
    def make_attrs_dict(name, min_val, max_val):
        min_val = round(min_val, ROUND_OFF_VALUE)
        max_val = round(max_val, ROUND_OFF_VALUE)

        attrs_dict = {
            'data-provide':      'slider',
            'data-slider-min':   min_val,
            'data-slider-max':   max_val,
            'data-slider-step':  STEP_VALUE,
            'data-slider-range': 'true',
            'data-slider-value': [min_val, max_val],
            'data-slider-id':    'id_' + name + '-wrapper'
            }
        return attrs_dict

    def __init__(self, feature_types, *args, **kwargs):
        super(ContentSearchForm, self).__init__(*args, **kwargs)
        feature_types = (list(feature_types))

        for feature in feature_types:
            name = feature.name
            group = feature.group
            min_val = feature.min_val
            max_val = feature.max_val
            disabled = True
            attrs_dict = self.make_attrs_dict(name, min_val, max_val)
            if name in self.data:
                disabled = False
                new_min_val, new_max_val = self.data[name].split(',')
                new_min_val = float(new_min_val)
                new_max_val = float(new_max_val)
                attrs_dict['data-slider-value'] = [new_min_val, new_max_val]
            widget = forms.TextInput(attrs=attrs_dict)
            self.fields[name] = CharFieldWithGroup(widget=widget,
                                                   required=False,
                                                   disabled=disabled,
                                                   group=group)
