from django import forms
from database.models import ExtractedFeature
from django.db.models import Max, Min
from database.widgets.range_slider import RangeSlider

ROUND_OFF_VALUE = 3


class CharFieldWithGroup(forms.CharField):
    def __init__(self, group, *args, **kwargs):
        super(CharFieldWithGroup, self).__init__(*args, **kwargs)
        self.group = group


class FeatureSearchForm(forms.Form):
    def __init__(self, feature_types, file_ids=None, *args, **kwargs):
        super(FeatureSearchForm, self).__init__(*args, **kwargs)
        extracted_features = ExtractedFeature.objects.filter(
            feature_of__id__in=file_ids
        )

        for feature in feature_types.iterator():
            if not file_ids:
                min_val = 0
                max_val = 0
            else:
                max_min_dict = extracted_features.filter(
                    instance_of_feature__name=feature.name
                ).aggregate(Min("value"), Max("value"))
                max_val = (
                    round(max_min_dict["value__max"][0],5) if max_min_dict["value__max"] else 0
                )
                min_val = (
                    round(max_min_dict["value__min"][0],5) if max_min_dict["value__min"] else 0
                )
            name = feature.name
            code = feature.code
            group = feature.group
            help_text = feature.description
            attrs = {
                "disabled": "true",
                "name": name,
                "code": code,
                "min": min_val,
                "max": max_val,
                "values": [min_val, max_val],
            }
            if code in self.data:
                new_min_val, new_max_val = self.data[code].split(",")
                attrs["disabled"] = "false"
                attrs["values"] = [round(float(new_min_val),5), round(float(new_max_val),5)]
            widget = RangeSlider(attrs=attrs)
            self.fields[name] = CharFieldWithGroup(
                widget=widget, required=False, group=group, help_text=help_text
            )
