from django.views.generic import DetailView, ListView
from database.models import TypeOfSection
from extra_views import SearchableListMixin


class TypeOfSectionDetailView(DetailView):
    model = TypeOfSection
    template_name = "detail.html"


class TypeOfSectionListView(SearchableListMixin, ListView):
    model = TypeOfSection
    search_fields = ["name"]
    queryset = TypeOfSection.objects.order_by("name")
    paginate_by = 100
    template_name = "list.html"
