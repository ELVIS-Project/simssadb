from django import forms
from database.widgets.multiple_entry_wiget import MultipleEntry


class CreationForm(forms.Form):
    attrs = {
            'name': 'variant_title',
            'class': 'form-control',
            'placeholder': 'e.g. Eroica'
            }
    widget = MultipleEntry(attrs=attrs)

    title = forms.CharField(label='Title',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'e.g. Symphony No.3 Op. 55'
                            }))
    variant_titles = forms.CharField(label='Variant Titles',
                                     widget=widget, required=False)
