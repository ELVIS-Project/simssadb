from urllib import request
from dal import autocomplete
from django import forms
from django.contrib.postgres.forms.ranges import IntegerRangeField
from database.models import (Archive, CollectionOfSources, Contribution,
                             GenreAsInStyle, GenreAsInType, GeographicArea,
                             Instrument, Part, Person, Section, Software)
from database.widgets.multiple_entry_wiget import MultipleEntry


class ContributionForm(forms.Form):
    person_given_name = forms.CharField(label="Person Given Name",
                                        required=True)
    person_surname = forms.CharField(label="Person Surname", required=False)
    person_range_date_birth = IntegerRangeField(label="Date of Birth",
                                                required=False)
    person_range_date_death = IntegerRangeField(label="Date of Death",
                                                required=False)

    role = forms.ChoiceField(
            choices=(
                ('COMPOSER', 'Composer'),
                ('ARRANGER', 'Arranger'),
                ('AUTHOR', 'Author of Text'),
                ('TRANSCRIBER', 'Transcriber'),
                ('IMPROVISER', 'Improviser'),
                ('PERFORMER', 'Performer')),)

    certainty_of_attribution = forms.NullBooleanField(
                                required=False,
                                widget=forms.RadioSelect(choices=(
                                        (True, "Certain"),
                                        (False, "Uncertain"),
                                        (None, "Unknown"))))
    location = forms.ModelChoiceField(
                required=False,
                queryset=GeographicArea.objects.all(),
                widget=autocomplete.ModelSelect2(
                    url='geographicarea-autocomplete',
                    attrs={'class': 'form-control'}))
    date = IntegerRangeField(required=False)


class CollectionOfSourcesForm(forms.Form):
    title = forms.CharField(label="Title of Collection *",
                            required=True)
    collection_url = forms.URLField(label="Collection URL (if applicable)",
                                    required=False)
    archive = forms.ModelChoiceField(
                        label="Archive/Library where this source can be found "
                        "(optional)",
                        required=False,
                        queryset=Archive.objects.all(),
                        widget=autocomplete.ModelSelect2(
                            url='archive-autocomplete',
                            attrs={'class': 'form-control'}))
    portions = forms.CharField(label="Portions",
                               required=False)


class WorkInfoForm(forms.Form):
    attrs = {
        'name': 'variant_title',
        'class': 'form-control',
        'placeholder': 'e.g. Eroica'
    }
    widget = MultipleEntry(attrs=attrs)

    title = forms.CharField(label='Title *',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'e.g. Symphony No.3 Op. 55'
                            }))

    variant_titles = forms.CharField(label='Variant Titles',
                                     widget=widget,
                                     required=False)

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
        'placeholder': 'e.g. I. Allegro con brio'
    }
    widget = MultipleEntry(attrs=attrs)
    sections = forms.CharField(label='Sections',
                               widget=widget,
                               required=False)


class FileForm(forms.Form):
    file = forms.FileField()
    software = forms.ModelChoiceField(
                            queryset=Software.objects.all(),
                            required=False,
                            widget=autocomplete.ModelSelect2(
                                url='software-autocomplete',
                                attrs={'class': 'form-control-file'}))
