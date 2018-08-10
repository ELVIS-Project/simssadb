from django.shortcuts import render
from django.views.generic import FormView
from haystack.query import SearchQuerySet

from database.forms.content_search_form import ContentSearchForm
from database.forms.faceted_search_form import FacetedSearchForm
from database.models import ExtractedFeature
from database.models import SymbolicMusicFile



    form_class = NiceFacetForm
class SearchView(FormView):
    context_object_name = 'object_list'
    facet_fields = ['religiosity', 'instruments',
                    'composers', 'types', 'styles',
                    'certainty', 'file_format']
    template_name = 'search/test.html'
