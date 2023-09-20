from urllib import request
from dal import autocomplete
from django import forms
from django.contrib.postgres.forms.ranges import IntegerRangeField
from database.models import (
    Archive,
    ContributionMusicalWork,
    File,
    GenreAsInStyle,
    GenreAsInType,
    GeographicArea,
    Instrument,
    Part,
    MusicalWork,
    Person,
    ResearchCorpus,
    Section,
    Software,
)
from django.db.models import CharField, Value, F
from database.widgets.multiple_entry_widget import MultipleEntry
from database.widgets.info_tooltip_widget import InfoTooltipWidget


class ContributionForm(forms.Form):

    birth_info = forms.CharField(
        label="",
        required=False,
        widget=InfoTooltipWidget(tooltip_text="Please enter the birth year of the contributor in either input box. If the specific year is not known, please enter a range."),
    )

    death_info = forms.CharField(
        label="",
        required=False,
        widget=InfoTooltipWidget(tooltip_text="Please enter the birth year of the contributor in either input box. If the specific year is not known, please enter a range."),
    )

    person_from_db_0 = forms.ModelMultipleChoiceField(
        label="Contributor's Name",
        required=False,
        queryset=Person.objects.all().order_by("surname"),
        widget=autocomplete.ModelSelect2(
            url="/person-autocomplete/", attrs={"class": "form-control autocomplete-select2",
                                                "name": "person_from_db_0"}
        ),
    )

    person_given_name_0 = forms.CharField(label="Contributor's Given Name*", required=False)
    
    person_surname_0 = forms.CharField(label="Contributor's Surname", required=False)
    
    person_range_date_birth_0 = IntegerRangeField(label="Date of Birth (range)*", required=False)
    
    person_range_date_death_0 = IntegerRangeField(label="Date of Death (range)*", required=False)
    
    role_0 = forms.ChoiceField(
        choices=(
            ("COMPOSER", "Composer"),
            ("ARRANGER", "Arranger"),
            ("AUTHOR", "Author of Text"),
            ("TRANSCRIBER", "Transcriber"),
            ("IMPROVISER", "Improviser"),
            ("PERFORMER", "Performer"),
        ),
        label="Role",
        required=False
    )

    certainty_of_attribution_0 = forms.NullBooleanField(
        required=False,
        widget=forms.RadioSelect(
            choices=((True, "Certain"), (False, "Uncertain"), (None, "Unknown"))
        ),
        label="Certainty of attribution"
    )

    location_0 = forms.ModelChoiceField(
        required=False,
        queryset=GeographicArea.objects.all().order_by("name"),
        widget=autocomplete.ModelSelect2(
            url="/geographicarea-autocomplete/", attrs={"class": "form-control autocomplete-select2",
                                                        "name": "location_0"}
        ),
        label="Location"
    )

    date_0 = IntegerRangeField(label="Date of Contribution (range)", required=False)
    
    person_from_db_1 = forms.ModelMultipleChoiceField(
        label="Contributor's Name",
        required=False,
        queryset=Person.objects.all().order_by("surname"),
        widget=autocomplete.ModelSelect2(
            url="/person-autocomplete/", attrs={"class": "form-control autocomplete-select2",
                                                "name": "person_from_db_1"}
        ),
    )

    person_given_name_1 = forms.CharField(label="Contributor's Given Name*", required=False)
    
    person_surname_1 = forms.CharField(label="Contributor's Surname", required=False)
    
    person_range_date_birth_1 = IntegerRangeField(label="Date of Birth (range)*", required=False)
    
    person_range_date_death_1 = IntegerRangeField(label="Date of Death (range)*", required=False)
    
    role_1 = forms.ChoiceField(
        choices=(
            ("COMPOSER", "Composer"),
            ("ARRANGER", "Arranger"),
            ("AUTHOR", "Author of Text"),
            ("TRANSCRIBER", "Transcriber"),
            ("IMPROVISER", "Improviser"),
            ("PERFORMER", "Performer"),
        ),
        label="Role",
        required=False
    )

    certainty_of_attribution_1 = forms.NullBooleanField(
        required=False,
        widget=forms.RadioSelect(
            choices=((True, "Certain"), (False, "Uncertain"), (None, "Unknown"))
        ),
        label="Certainty of attribution"
    )

    location_1 = forms.ModelChoiceField(
        required=False,
        queryset=GeographicArea.objects.all().order_by("name"),
        widget=autocomplete.ModelSelect2(
            url="/geographicarea-autocomplete/", attrs={"class": "form-control autocomplete-select2",
                                                        "name": "location_1"}
        ),
        label="Location"
    )

    date_1 = IntegerRangeField(label="Date of Contribution (range)", required=False)
    
    person_from_db_2 = forms.ModelMultipleChoiceField(
        label="Contributor's Name",
        required=False,
        queryset=Person.objects.all().order_by("surname"),
        widget=autocomplete.ModelSelect2(
            url="/person-autocomplete/", attrs={"class": "form-control autocomplete-select2",
                                                "name": "person_from_db_2"}
        ),
    )

    person_given_name_2 = forms.CharField(label="Contributor's Given Name*", required=False)
    
    person_surname_2 = forms.CharField(label="Contributor's Surname", required=False)
    
    person_range_date_birth_2 = IntegerRangeField(label="Date of Birth (range)*", required=False)
    
    person_range_date_death_2 = IntegerRangeField(label="Date of Death (range)*", required=False)
    
    role_2 = forms.ChoiceField(
        choices=(
            ("COMPOSER", "Composer"),
            ("ARRANGER", "Arranger"),
            ("AUTHOR", "Author of Text"),
            ("TRANSCRIBER", "Transcriber"),
            ("IMPROVISER", "Improviser"),
            ("PERFORMER", "Performer"),
        ),
        label="Role",
        required=False
    )

    certainty_of_attribution_2 = forms.NullBooleanField(
        required=False,
        widget=forms.RadioSelect(
            choices=((True, "Certain"), (False, "Uncertain"), (None, "Unknown"))
        ),
        label="Certainty of attribution"
    )

    location_2 = forms.ModelChoiceField(
        required=False,
        queryset=GeographicArea.objects.all().order_by("name"),
        widget=autocomplete.ModelSelect2(
            url="/geographicarea-autocomplete/", attrs={"class": "form-control autocomplete-select2",
                                                        "name": "location_2"}
        ),
        label="Location"
    )

    date_2 = IntegerRangeField(label="Date of Contribution (range)", required=False)
    
  
class WorkInfoForm(forms.Form):
    
    contribution_tooltips = forms.CharField(
        label="",
        required=False,
        widget=InfoTooltipWidget(tooltip_text="This field is not required if the musical work already exists in the database. If you are creating a new musical work, please input the contributor's name, year of birth, and year of death."),
    )
    attrs = {
        "name": "variant_title",
        "class": "form-control",
        "placeholder": "e.g. Eroica",
    }
    
    variant_titles = forms.CharField(
        label="Variant Titles", widget=MultipleEntry(attrs=attrs), required=False
    )
    
    variant_titles_from_db = forms.CharField(
        label="Variant Titles", widget=MultipleEntry(attrs = {
            "name": "variant_title_from_db",
            "class": "form-control",
            "placeholder": "e.g. Eroica",
        }), required=False
    )

    variant_titles_from_db_tooltips = forms.CharField(
        label="",
        required=False,
        widget=InfoTooltipWidget(tooltip_text="Input new titles to be added to the musical work."),
    )

    title = forms.CharField(
        label="Title*",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g. Symphony No.3 Op. 55"}
        ),
        required=False
    )

    title_from_db = forms.ModelMultipleChoiceField(
        label="Title*",
        required=False,
        queryset=MusicalWork.objects.annotate(
            first_variant_title=F('variant_titles__0')
        ).order_by('first_variant_title'),
        widget=autocomplete.ModelSelect2(
            url="/musicalwork-autocomplete/", attrs={"class": "form-control autocomplete-select2", "name": "title_from_db"}
        ),
    )

    title_from_db_tooltips = forms.CharField(
        label="",
        required=False,
        widget=InfoTooltipWidget(tooltip_text="Can't find what you're looking for? Click the checkbox below."),
    )
    
    genre_as_in_style = forms.ModelMultipleChoiceField(
        required=False,
        queryset=GenreAsInStyle.objects.all(),
        widget=autocomplete.ModelSelect2(#Multiple(
            url="/style-autocomplete/", attrs={"class": "form-control"}
        ),
    )

    genre_as_in_type = forms.ModelMultipleChoiceField(
        required=False,
        queryset=GenreAsInType.objects.all().order_by("name"),
        widget=autocomplete.ModelSelect2(#Multiple(
            url="/type-autocomplete/", attrs={"class": "form-control autocomplete-select2"}
        ),
    )

    sacred_or_secular = forms.ChoiceField(
        required=False,
        label="Sacred Or Secular",
        choices=(
            (None, "------"),
            (None, "Not Applicable"),
            (True, "Sacred"),
            (False, "Secular"),
        ),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    instruments = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Instrument.objects.all().order_by("name"),
        widget=autocomplete.ModelSelect2Multiple(
            url="/instrument-autocomplete/", attrs={"class": "form-control autocomplete-select2"}
        ),
    )

    sections = forms.CharField(
        label="Sections",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. I. Allegro con brio",
            }
        ),
    )
    select_section = forms.ChoiceField(
        choices=[
            ('1', '1. Kyrie'),
            ('2', '2. Gloria'),
            ('3', '3. Credo'),
            ('4', '4. Sanctus'),
            ('5', '5. Agnus'),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )

    sections_from_db = forms.CharField(
        label="Sections",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. I. Allegro con brio",
            }
        ),
    )
    select_section_from_db = forms.ChoiceField(
        choices=[
            ('1', '1. Kyrie'),
            ('2', '2. Gloria'),
            ('3', '3. Credo'),
            ('4', '4. Sanctus'),
            ('5', '5. Agnus'),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    sections_from_db_tooltips = forms.CharField(
        label="",
        required=False,
        widget=InfoTooltipWidget(tooltip_text="Input sections to be added to the musical work. Please only input new sections. If the section you are looking for already exists, please skip this section."),
    )
    

class FileForm(forms.Form):
    file = forms.FileField(max_length=255, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                           required=False)
    software = forms.ModelChoiceField(
        queryset=Software.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(
            url="/software-autocomplete/", attrs={"class": "form-control-file form-control"}
        ),
    )
    TYPES = (
        ("sym", "Symbolic Music"),
        ("txt", "Text"),
        ("img", "Image"),
        ("audio", "Audio"),
    )
    file_type = forms.ChoiceField(
        label="Source Type",
        choices=TYPES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class SourceForm(forms.Form):
    url = forms.CharField(
        label="URL linking to source",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    title = forms.CharField(
        label="Title of source",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    archive = forms.CharField(
        label="Archive where source is located",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    