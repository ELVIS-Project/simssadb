from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from haystack.forms import SearchForm, FacetedSearchForm
from database.models.person import Person
from database.models.musical_work import MusicalWork
from database.models.geographic_area import GeographicArea
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.genre_as_in_type import GenreAsInType
from database.models.contribution import Contribution
from database.models.part import Part
from database.models.collection_of_sources import CollectionOfSources
from database.models.source import Source


class SourcesForm(forms.ModelForm):
    class Meta:
        model = Source
        exclude = ()


class CollectionOfSourcesForm(forms.ModelForm):
    class Meta:
        model = CollectionOfSources
        exclude = ()


class MusicalWorkForm(forms.ModelForm):
    class Meta:
        model = MusicalWork
        exclude = ('authority_control_key',)


class GeographicAreaForm(forms.ModelForm):
    class Meta:
        model = GeographicArea
        exclude = ('authority_control_key',)


class GenreStyleForm(forms.ModelForm):
    class Meta:
        model = GenreAsInStyle
        exclude = ()


class GenreTypeForm(forms.ModelForm):
    class Meta:
        model = GenreAsInType
        exclude = ()


class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        exclude = ()


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        exclude = ()


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('authority_control_key', 'parts_contributed_to', 'sections_contributed_to', 'works_contributed_to',)


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Shows when the blank is empty.
        # If not used, the blank will show the name of field as default
        self.fields["username"].label = "Display name"


class FuzzySearchForm(SearchForm):
    """A form that does fuzzy searches by default"""

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get("q"):
            return self.no_query_found()

        query = self.cleaned_data['q']
        sqs = self.searchqueryset.filter(text__fuzzy=query)

        if self.load_all:
            sqs = sqs.load_all()

        return sqs


class FacetedWorkSearchForm(FuzzySearchForm):

    def __init__(self, *args, **kwargs):
        data = dict(kwargs.get("data", []))
        self.selected_facets = kwargs.pop("selected_facets", [])
        self.places = data.get('places', [])
        self.dates = data.get('dates', [])
        self.sym_formats = data.get('sym_formats', [])
        self.audio_formats = data.get('audio_formats', [])
        self.text_formats = data.get('text_formats', [])
        self.image_formats = data.get('image_formats', [])
        self.certainty = data.get('certainty', [])
        self.languages = data.get('languages', [])
        self.religiosity = data.get('religiosity', [])
        self.instruments = data.get('instruments', [])
        self.composers = data.get('composers', [])
        self.types = data.get('types', [])
        self.styles = data.get('styles', [])
        self.facets = ['places', 'dates', 'sym_formats', 'audio_formats',
                       'text_formats', 'image_formats', 'certainty',
                       'languages', 'religiosity', 'instruments', 'composers',
                       'types', 'styles']
        super(FacetedWorkSearchForm, self).__init__(*args, **kwargs)

    def _narrow_by(self, sqs, field):
        facet = getattr(self, field)
        if facet:
            query = None
            for value in self.facet:
                if query:
                    query += ' OR '
                else:
                    query = ''
                query += '"%s"' % sqs.query.clean(value)
            sqs = sqs.narrow('{0}:{1}'.format(field, query))
        return sqs

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get("q"):
            return self.no_query_found()

        query = self.cleaned_data['q']
        sqs = self.searchqueryset.models(MusicalWork).filter(text__fuzzy=query)

        if self.load_all:
            sqs = sqs.load_all()

        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow('%s:"%s"' % (field, sqs.query.clean(value)))

        for facet in self.facets:
            sqs = self._narrow_by(sqs, facet)

        return sqs
