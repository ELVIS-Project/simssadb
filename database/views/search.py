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
    search_queryset = SearchQuerySet().models(SymbolicMusicFile).all()
    queryset = None
    names = set(ExtractedFeature.objects.
                filter(value__len__lt=2).
                values_list('name', flat=True))

    @staticmethod
    def faceted_search(facets, query, search_queryset, request):
        search_queryset = search_queryset.filter(text__fuzzy=query)

        kwargs = {}
        for facet in facets:
            chosen = request.GET.getlist(facet)
            if chosen:
                key = facet + '__in'
                key_value_pair = {key: chosen}
                kwargs.update(key_value_pair)
        if kwargs:
            search_queryset = search_queryset.filter(**kwargs)

        return set(map(lambda x: int(x),
                       (search_queryset.values_list('pk', flat=True))))
    @staticmethod
    def content_search(request, names):

        def single_feature_search(name, min_val, max_val):
            file_ids = list(ExtractedFeature.objects.filter(
                    name__exact=name,
                    value__0__gte=min_val,
                    value__0__lte=max_val
                    ).values_list('feature_of_id', flat=True))
            return file_ids

        file_id_set = set(SymbolicMusicFile.objects.values_list('id',
                                                                flat=True))

        if any(key in names for key in request.GET):
            for key, value in request.GET.lists():
                if key in names:
                    min_value, max_value = value[0].split(',')
                    single_feature_results = single_feature_search(key,
                                                                   min_value,
                                                                   max_value)
                    file_id_set = file_id_set.intersection(
                        set(single_feature_results))
        return file_id_set
