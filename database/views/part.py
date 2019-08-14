from django.views.generic import DetailView, ListView
from database.models import Part
from extra_views import SearchableListMixin


class PartDetailView(DetailView):
    model = Part
    context_object_name = "part"


class PartListView(SearchableListMixin, ListView):
    model = Part
    search_fields = ["written_for__name"]
    queryset = Part.objects.order_by("written_for__name")
    paginate_by = 100
    template_name = "list.html"
