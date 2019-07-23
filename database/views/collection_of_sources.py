from django.views.generic import DetailView, ListView
from database.models import CollectionOfSources
from extra_views import SearchableListMixin


class CollectionOfSourcesDetailView(DetailView):
    model = CollectionOfSources
    context_object_name = "collection_of_sources"


class CollectionOfSourcesListView(SearchableListMixin, ListView):
    model = CollectionOfSources
    search_fields = ["title"]
    queryset = CollectionOfSources.objects.order_by("title")
    paginate_by = 100
    template_name = "list.html"
