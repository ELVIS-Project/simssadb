from django.views.generic import DetailView, ListView
from database.models import Source
from extra_views import SearchableListMixin


class SourceDetailView(DetailView):
    model = Source
    context_object_name = "source"


class SourceListView(SearchableListMixin, ListView):
    model = Source
    search_fields = ["collection__title"]
    queryset = Source.objects.order_by("collection__title")
    paginate_by = 100
    template_name = "list.html"
