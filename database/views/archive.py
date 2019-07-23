from django.views.generic import DetailView, ListView
from database.models import Archive
from extra_views import SearchableListMixin


class ArchiveDetailView(DetailView):
    model = Archive
    template_name = "detail.html"


class ArchiveListView(SearchableListMixin, ListView):
    model = Archive
    search_fields = ["name"]
    queryset = Archive.objects.order_by("name")
    paginate_by = 100
    template_name = "list.html"
