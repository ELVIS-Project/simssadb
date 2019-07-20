from django.views.generic import DetailView, ListView
from database.models import ExtractedFeature
from extra_views import SearchableListMixin


class ExtractedFeatureDetailView(DetailView):
    model = ExtractedFeature
    template_name = "detail.html"


class ExtractedFeatureListView(SearchableListMixin, ListView):
    model = ExtractedFeature
    search_fields = ["name"]
    queryset = ExtractedFeature.objects.order_by("instance_of_feature__name")
    paginate_by = 100
    template_name = "list.html"
