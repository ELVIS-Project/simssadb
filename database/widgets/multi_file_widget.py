from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe


class MultipleFile(Widget):
    template_name = 'widgets/multiple_file_widget.html'

    def __init__(self, attrs):
        self.attrs = attrs

    def get_context(self, name, value, attrs):
        return attrs

    def render(self, name, value, attrs=None, **kwargs):
        context = self.get_context(name, value, self.attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
