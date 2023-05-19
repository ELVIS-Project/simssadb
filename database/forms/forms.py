from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from database.models.person import Person
from database.models.musical_work import MusicalWork
from database.models.geographic_area import GeographicArea
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.genre_as_in_type import GenreAsInType
from database.models.contribution_musical_work import ContributionMusicalWork
from database.models.part import Part
from database.models.source import Source
from database.models.section import Section
from database.models.research_corpus import ResearchCorpus


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        exclude = ()


class SourcesForm(forms.ModelForm):
    class Meta:
        model = Source
        exclude = ()


class MusicalWorkForm(forms.ModelForm):
    class Meta:
        model = MusicalWork
        exclude = ()


class GeographicAreaForm(forms.ModelForm):
    class Meta:
        model = GeographicArea
        exclude = ()


class GenreStyleForm(forms.ModelForm):
    class Meta:
        model = GenreAsInStyle
        exclude = ()


class GenreTypeForm(forms.ModelForm):
    class Meta:
        model = GenreAsInType
        exclude = ()


class ContributionMusicalWorkForm(forms.ModelForm):
    class Meta:
        model = ContributionMusicalWork
        exclude = ()


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        exclude = ()


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = (
            "parts_contributed_to",
            "sections_contributed_to",
            "works_contributed_to",
        )


# defined in creation_forms.py ...?
# class ResearchCorpusForm(forms.ModelForm):
#     class Meta:
#         model = ResearchCorpus
#         exclude = ()


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Shows when the blank is empty.
        # If not used, the blank will show the name of field as default
        self.fields["username"].label = "Display name"
