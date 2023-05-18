from django import forms
from database.models import Source


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['title', 'date_range_year_only', 'source_type', 'in_archive', 'languages', 'url']
