from haystack.generic_views import FacetedSearchView
from database.forms import FuzzySearchForm, FacetedWorkSearchForm, FacetedSearchForm
from database.forms.faceting import NiceFacetForm
from haystack.query import SearchQuerySet
PAGE_SIZE = 25


class GeneralSearch(FacetedSearchView):
    facet_fields = ['places', 'dates', 'sym_formats', 'audio_formats',
                    'text_formats', 'image_formats', 'certainty',
                    'languages', 'religiosity', 'instruments',
                    'composers', 'types', 'styles']
    context_object_name = 'object_list'
    template_name = 'search/search.html'
    form_class = FacetedWorkSearchForm
    paginate_by = PAGE_SIZE


class TestFacet(FacetedSearchView):
    form_class = NiceFacetForm
    context_object_name = 'object_list'
    facet_fields = ['places', 'dates', 'sym_formats', 'audio_formats',
                    'text_formats', 'image_formats', 'certainty',
                    'languages', 'religiosity', 'instruments',
                    'composers', 'types', 'styles']
    selected_facets = ['places', 'dates', 'sym_formats', 'audio_formats',
                       'text_formats', 'image_formats', 'certainty',
                       'languages', 'religiosity', 'instruments',
                       'composers', 'types', 'styles']
    template_name = 'search/test.html'
    paginate_by = PAGE_SIZE
