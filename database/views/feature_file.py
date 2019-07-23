from django.views.generic import DetailView, ListView
from database.models import FeatureFile
from extra_views import SearchableListMixin


class FeatureFileDetailView(DetailView):
    model = FeatureFile
    template_name = "detail.html"


class FeatureFileListView(SearchableListMixin, ListView):
    model = FeatureFile
    search_fields = ["file_type"]
    queryset = FeatureFile.objects.order_by("id")
    paginate_by = 100
    template_name = "list.html"
