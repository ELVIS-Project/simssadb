from django.views.generic import DetailView, ListView
from database.models import Software
from extra_views import SearchableListMixin


class SoftwareDetailView(DetailView):
    model = Software
    template_name = "detail.html"


class SoftwareListView(SearchableListMixin, ListView):
    model = Software
    search_fields = ["name"]
    queryset = Software.objects.order_by("name")
    paginate_by = 100
    template_name = "list.html"
