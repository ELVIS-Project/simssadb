from django.views.generic import DetailView, ListView
from database.models import GeographicArea
from extra_views import SearchableListMixin

class GeographicAreaDetailView(DetailView):
    model = GeographicArea
    context_object_name = "geographic_area"


class GeographicAreaListView(SearchableListMixin, ListView):
    model = GeographicArea
    search_fields = ["name"]
    queryset = GeographicArea.objects.order_by("name")
    paginate_by = 100
    template_name = "list.html"
