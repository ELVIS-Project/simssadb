from haystack.generic_views import FacetedSearchView

from database.forms.faceting import NiceFacetForm

PAGE_SIZE = 25


class TestFacet(FacetedSearchView):
    form_class = NiceFacetForm
    context_object_name = 'object_list'
    facet_fields = ['places', 'dates', 'sym_formats', 'audio_formats',
                    'text_formats', 'image_formats', 'certainty',
                    'languages', 'religiosity', 'instruments',
                    'composers', 'types', 'styles']
    template_name = 'search/test.html'
    paginate_by = PAGE_SIZE
