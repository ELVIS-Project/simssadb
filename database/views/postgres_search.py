
class PostgresSearchView(ListView):
    model = MusicalWork
    context_object_name = "works"
    template_name = "search/pg_search.html"

    def get_queryset(self):
        query_string = self.request.GET.get("q")
        if not query_string:
            return MusicalWork.objects.none()
        query = SearchQuery(query_string)
        rank_annotation = SearchRank(F("search_document"), query)
        query_set = (
            MusicalWork.objects.annotate(rank=rank_annotation)
            .filter(search_document=query)
            .order_by("-rank")
        )
        return query_set

