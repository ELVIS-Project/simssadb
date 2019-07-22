from django.views.generic import DetailView, ListView
from database.models import Institution
from extra_views import SearchableListMixin


class InstitutionDetailView(DetailView):
    model = Institution
    template_name = "detail.html"


class InstitutionListView(SearchableListMixin, ListView):
    model = Institution
    search_fields = ["name"]
    queryset = Institution.objects.order_by("name")
    paginate_by = 100
    template_name = "list.html"
