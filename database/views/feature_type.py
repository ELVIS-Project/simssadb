from django.views.generic import DetailView, ListView
from database.models import FeatureType
from extra_views import SearchableListMixin


class FeatureTypeDetailView(DetailView):
    model = FeatureType
    template_name = "detail.html"


class FeatureTypeListView(SearchableListMixin, ListView):
    model = FeatureType
    search_fields = ["name"]
    queryset = FeatureType.objects.order_by("code")
    paginate_by = 100
    template_name = "list.html"
