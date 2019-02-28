from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe


class RangeSlider(Widget):
    template_name = 'widgets/range_slider.html'
    gradation = 100

    def __init__(self, attrs):
        self.attrs = attrs

    def get_context(self, name, value, attrs):
        return {
            'widget': {
                'name':      name,
                'code':      attrs['code'],
                'min':       attrs['min'],
                'max':       attrs['max'],
                'disabled':  attrs['disabled'],
                'values':    attrs['values'],
                'gradation': self.gradation,
                }
            }

    def render(self, name, value, attrs=None, **kwargs):
        context = self.get_context(name, value, self.attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
