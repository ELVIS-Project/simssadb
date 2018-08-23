from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from database.models import ContributedTo
from database.models import GenreAsInStyle
from database.models.genre_as_in_type import GenreAsInType
from database.models import GeographicArea
from database.models import Person
from database.models import Source
from database.models import Part
from database.models import Section
from database.models import Instrument


class MusicalWorkCreationForm(forms.Form):
    title = SimpleArrayField(base_field=forms.CharField(max_length=100),
                             delimiter='/')
    genres_as_in_style = forms.ModelMultipleChoiceField(
            queryset=GenreAsInStyle.objects.all())
    genres_as_in_type = forms.ModelMultipleChoiceField(
            queryset=GenreAsInType.objects.all())
    number_of_sections = forms.IntegerField(min_value=1, initial=1)
    sacred_or_secular = forms.NullBooleanField()
    instrumentation = forms.ModelMultipleChoiceField(
            queryset=Instrument.objects.all())


class SectionCreationForm(forms.Form):
    title = forms.CharField(max_length=100)
    ordering = forms.IntegerField(min_value=1)


class ContributionCreationForm(forms.Form):
    choices = ContributedTo.ROLES
    role = forms.ChoiceField(choices=choices, initial=choices[0])
    person = forms.ModelChoiceField(queryset=Person.objects.all())
    date_start = forms.IntegerField(min=0, initial=1400)
    date_end = forms.IntegerField(min=0, initial=1405)
    location = forms.ModelChoiceField(queryset=GeographicArea.objects.all())


class FileCreationForm(forms.Form):
    file = forms.FileField()
    source = forms.ModelChoiceField(queryset=Source.objects.all())
    attach_to_work = forms.BooleanField()
    attach_to_sections = forms.ModelChoiceField(queryset=Section.objects.all())
    attach_to_parts = forms.ModelChoiceField(queryset=Part.objects.all())
