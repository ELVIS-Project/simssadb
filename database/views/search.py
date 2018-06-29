from haystack.generic_views import SearchView

from database.forms import FuzzySearchForm


class GeneralSearch(SearchView):
    template_name = 'search/general-search.html'
    form_class = FuzzySearchForm
