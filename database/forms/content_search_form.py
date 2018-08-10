from django import forms
import pprint as pp
from database.models import ExtractedFeature

ROUND_OFF_VALUE = 3
STEP_VALUE = 0.001


class ContentSearchForm(forms.Form):

    @staticmethod
    def make_attrs_dict(name, min_val, max_val):
        min_val = round(min_val[0], ROUND_OFF_VALUE)
        max_val = round(max_val[0], ROUND_OFF_VALUE)

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

    def __init__(self, names, *args, **kwargs):
        super(ContentSearchForm, self).__init__(*args, **kwargs)
        pp.pprint(self.data)
        names = (list(names))
        names.sort()

        for name in names:
            min_max = ExtractedFeature.objects.min_and_max(name)
            min_val = min_max['min_val']
            max_val = min_max['max_val']
            disabled = True
            attrs_dict = self.make_attrs_dict(name, min_val, max_val)
            if name in self.data:
                disabled = False
                new_min_val, new_max_val = self.data[name].split(',')
                new_min_val = float(new_min_val)
                new_max_val = float(new_max_val)
                attrs_dict['data-slider-value'] = [new_min_val, new_max_val]
                pp.pprint(attrs_dict)
            widget = forms.TextInput(attrs=attrs_dict)
            self.fields[name] = forms.CharField(widget=widget, required=False,
                                                disabled=disabled)
