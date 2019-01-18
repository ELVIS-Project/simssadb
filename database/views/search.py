from django.shortcuts import render
from django.views.generic import FormView
from haystack.query import SearchQuerySet

from database.forms.content_search_form import ContentSearchForm
from database.forms.faceted_search_form import FacetedSearchForm
from database.models import ExtractedFeature
from database.models import FeatureType
from database.models import SymbolicMusicFile
from database.utils.view_utils import make_summary_dict


# TODO: add comments to explain algorithms and choices


class SearchView(FormView):
    facets = ['sacred_or_secular', 'instruments',
              'composers', 'types', 'styles',
              'certainty', 'file_format']
    template_name = 'search/search.html'
    search_queryset = SearchQuerySet().models(SymbolicMusicFile).all()
    queryset = None
    feature_types = FeatureType.objects.exclude(dimensions__gt=1)
    codes = feature_types.values_list('code', flat=True)
    summary_fields = ['file_type', 'file_size', 'source']

    @staticmethod
    def faceted_search(facets, query, search_queryset, request) -> set:
        """Filter a queryset based on user-chosen facets.

        Parameters
        ----------
        facets : list
            A list of strings specifying the facets to filter by
        query : str
            The user query string
        search_queryset : SearchQuerySet
            The SearchQuerySet to be filtered
        request : django.http.request HttpRequest

        Returns
        -------
        set
            A set with all the primary keys of objects that matched the query
            and facets

        """
        # First get everything that (fuzzy) matches our query
        search_queryset = search_queryset.filter(text__fuzzy=query)

        # Then we need to filter by facet
        kwargs = {}  # Dict to hold our (facet : value) pairs
        for facet in facets:
            value = request.GET.getlist(facet)
            if value:
                key = facet + '__in'  # Add __in to filter the queryset
                key_value_pair = {key: value}
                kwargs.update(key_value_pair)

        # Use the dict above to filter the queryset
        if kwargs:
            search_queryset = search_queryset.filter(**kwargs)

        # To return we take all the primary keys of the search_queryset,
        # convert them into ints and then make a set out of them (so there are
        # no repetitions)
        return set(map(lambda x: int(x),
                       (search_queryset.values_list('pk', flat=True))))

    @staticmethod
    def content_search(request, codes):

        def single_feature_search(code, min_val, max_val):
            file_ids = list(ExtractedFeature.objects.filter(
                    instance_of_feature__code=code,
                    value__0__gte=min_val,
                    value__0__lte=max_val
                    ).values_list('feature_of_id', flat=True))
            return file_ids

        file_id_set = set(SymbolicMusicFile.objects.values_list('id',
                                                                flat=True))

        if any(key in codes for key in request.GET):
            for key, value in request.GET.lists():
                if key in codes:
                    min_value, max_value = value[0].split(',')
                    single_feature_results = single_feature_search(key,
                                                                   min_value,
                                                                   max_value)
                    file_id_set = file_id_set.intersection(
                            set(single_feature_results))
        return file_id_set

    # TODO: make this more robust, specially when no query
    # TODO: add validation
    def get(self, request, *args, **kwargs):
        query = request.GET['q']

        faceted_search_results = self.faceted_search(
                facets=self.facets,
                query=query,
                search_queryset=self.search_queryset,
                request=request
                )
        content_search_results = self.content_search(request, self.codes)

        merged_result_ids = faceted_search_results.intersection(
                content_search_results)

        files_queryset = SymbolicMusicFile.objects.filter(
                id__in=merged_result_ids)
        files = []

        for file in files_queryset:
            new_element = make_summary_dict(file, self.summary_fields)
            new_element['display'] = file.musical_work.display_name
            new_element['file'] = file.display_name
            files.append(new_element)

        ids_for_sqs = list(map(lambda x: str(x), merged_result_ids))

        self.search_queryset = SearchQuerySet().models(
                SymbolicMusicFile).filter(django_id__in=ids_for_sqs)

        context = {
            'content_search_form': ContentSearchForm(
                    feature_types=self.feature_types,
                    data=request.GET),
            'faceted_search_form': FacetedSearchForm(
                    selected_facets=self.facets,
                    search_queryset=self.search_queryset,
                    data=request.GET),
            }

        search_results = {
            'list':        files,
            'model_name':  'Files',
            'model_count': files_queryset.count(),
            'query':       query
            }

        context.update(search_results)

        return render(request, self.template_name, context)
