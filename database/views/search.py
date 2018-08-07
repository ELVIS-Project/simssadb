from haystack.generic_views import FacetedSearchView

from database.forms.faceting import NiceFacetForm

PAGE_SIZE = 25


class TestFacet(FacetedSearchView):
    form_class = NiceFacetForm
    context_object_name = 'object_list'
    facet_fields = ['religiosity', 'instruments',
                    'composers', 'types', 'styles',
                    'certainty']
    template_name = 'search/test.html'
    paginate_by = PAGE_SIZE
