from django import forms
from database.widgets.multiple_entry_wiget import MultipleEntry
from database.models import Instrument, GenreAsInStyle, GenreAsInType
from dal import autocomplete as ac


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

    instrument = forms.ModelChoiceField(queryset=Instrument.objects.all(),
                                        widget=ac.ModelSelect2Multiple(
                                            url='instrument-autocomplete'))

    type_ = forms.ModelChoiceField(queryset=GenreAsInType.objects.all(),
                                   widget=ac.ModelSelect2Multiple(
                                       url='instrument-autocomplete'))

    style = forms.ModelChoiceField(queryset=GenreAsInStyle.objects.all(),
                                   widget=ac.ModelSelect2Multiple(
                                       url='style-autocomplete'))
