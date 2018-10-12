import json

from django.forms import MultiWidget


class MultiFieldWidget(MultiWidget):

    def __init__(self, field_widgets, attrs=None):
        super().__init__(field_widgets, attrs)

    def decompress(self, value):
        if value:
            dict_value = json.loads(value)
            return dict_value
        return ""
