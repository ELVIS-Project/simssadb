from django import forms
from database.widgets.multiple_entry_wiget import MultipleEntry
from dal import autocomplete
from database.models import GenreAsInStyle, GenreAsInType, Instrument, CollectionOfSources


class WorkInfoForm(forms.Form):
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

    genre_as_in_style = forms.ModelMultipleChoiceField(queryset=GenreAsInStyle.objects.all(),
                                                       widget=autocomplete.ModelSelect2Multiple(
                                                            url='style-autocomplete', attrs={'class': 'form-control'}))

    genre_as_in_type = forms.ModelMultipleChoiceField(queryset=GenreAsInType.objects.all(),
                                                      widget=autocomplete.ModelSelect2Multiple(
                                                           url='type-autocomplete', attrs={'class': 'form-control'}))

    sacred_or_secular = forms.ChoiceField(choices=((None, '------'), (None, 'Not Applicable'), (True, 'Sacred'),
                                                   (False, 'Secular')),
                                          widget=forms.Select(attrs={'class': 'form-control'}))

    instruments = forms.ModelMultipleChoiceField(queryset=Instrument.objects.all(),
                                                 widget=autocomplete.ModelSelect2Multiple(
                                                     url='instrument-autocomplete', attrs={'class': 'form-control'}))

    attrs = {
        'name': 'section_title',
        'class': 'form-control',
        'placeholder': 'e.g. Allegro con brio'
    }
    widget = MultipleEntry(attrs=attrs)
    sections = forms.CharField(label='Sections',
                                     widget=widget, required=False)
