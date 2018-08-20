from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from haystack.forms import SearchForm, FacetedSearchForm
from django.utils.translation import ugettext_lazy as _
from database.models.person import Person
from database.models.genre import Genre
from database.models.musical_work import MusicalWork
from database.models.geographic_area import GeographicArea

class MusicalWorkForm(forms.ModelForm):

    class Meta:
        model = MusicalWork
        exclude = ('authority_control_key',)


class GeographicAreaForm(forms.ModelForm):

    class Meta:
        model = GeographicArea
        exclude = ('authority_control_key',)


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = ('authority_control_key', 'parts_contributed_to', 'sections_contributed_to', 'works_contributed_to', )


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Shows when the blank is empty.
        # If not used, the blank will show the name of field as default
        self.fields["username"].label = "Display name"


