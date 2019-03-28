from django import forms
from database.widgets.multiple_entry_wiget import MultipleEntry
from dal import autocomplete
from database.models import GenreAsInStyle, GenreAsInType, Instrument, \
        CollectionOfSources, Contribution, Software, Archive, GeographicArea


class ContributionForm(forms.ModelForm):
    class Meta:
            model = Contribution
            fields = ['person', 'certainty_of_attribution',
                      'role', '_date', 'location']


class CollectionOfSourcesForm(forms.Form):
    title = forms.CharField(label="Title of Collection (if applicable)",
                            required=False)
    source_url = forms.URLField(label="Source URL (if applicable)",
                                required=False)
    collection_url = forms.URLField(label="Collection URL (if applicable)",
                                    required=False)
    comments = forms.Textarea()
    place_of_publication = forms.ModelMultipleChoiceField(
                            label="Place of publication or creation",
                            queryset=GeographicArea.objects.all(),
                            required=False,
                            widget=autocomplete.ModelSelect2(
                                url='archive-autocomplete',
                                attrs={'class': 'form-control'}))
    archive = forms.ModelMultipleChoiceField(
                        label="Archive/Library where this source can be found "
                        "(optional)",
                        required=False,
                        queryset=Archive.objects.all(),
                        widget=autocomplete.ModelSelect2(
                            url='archive-autocomplete',
                            attrs={'class': 'form-control'}))
    portions = forms.CharField(label="Portions", required=False)


class FileForm(forms.Form):
    file = forms.FileField()
    attach_to = forms.CharField(label='Attach To')
    software = forms.ModelMultipleChoiceField(
                            queryset=Software.objects.all(),
                            required=False,
                            widget=autocomplete.ModelSelect2Multiple(
                                url='software-autocomplete',
                                attrs={'class': 'form-control'}))


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

    genre_as_in_style = forms.ModelMultipleChoiceField(
                            required=False,
                            queryset=GenreAsInStyle.objects.all(),
                            widget=autocomplete.ModelSelect2Multiple(
                                url='style-autocomplete',
                                attrs={'class': 'form-control'}))

    genre_as_in_type = forms.ModelMultipleChoiceField(
                            required=False,
                            queryset=GenreAsInType.objects.all(),
                            widget=autocomplete.ModelSelect2Multiple(
                                url='type-autocomplete',
                                attrs={'class': 'form-control'}))

    sacred_or_secular = forms.ChoiceField(
                                required=False,
                                label="Sacred Or Secular",
                                choices=(
                                    (None, '------'),
                                    (None, 'Not Applicable'),
                                    (True, 'Sacred'),
                                    (False, 'Secular')),
                                widget=forms.Select(
                                    attrs={'class': 'form-control'}))

    instruments = forms.ModelMultipleChoiceField(
                            required=False,
                            queryset=Instrument.objects.all(),
                            widget=autocomplete.ModelSelect2Multiple(
                                    url='instrument-autocomplete',
                                    attrs={'class': 'form-control'}))

    attrs = {
        'name': 'section_title',
        'class': 'form-control',
        'placeholder': 'e.g. Allegro con brio'
    }
    widget = MultipleEntry(attrs=attrs)
    sections = forms.CharField(label='Sections',
                                     widget=widget, required=False)
