from django.shortcuts import render
from django.views.generic import FormView
from haystack.query import SearchQuerySet

from database.forms.content_search_form import ContentSearchForm
from database.forms.faceted_search_form import FacetedSearchForm
from database.models import ExtractedFeature
from database.models import SymbolicMusicFile

# TODO: add comments to explain algorithms and choices


class SearchView(FormView):
    facets = ['religiosity', 'instruments',
              'composers', 'types', 'styles',
              'certainty', 'file_format']
    template_name = 'search/search.html'
