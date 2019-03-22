from django import forms
from database.models import CollectionOfSources


class SourceForm(forms.ModelForm):
    class Meta:
        model = CollectionOfSources
        fields = ['title', 'date', 'person_publisher', 'institution_publisher', 'url']
