from django.views.generic import DetailView, ListView
from database.models import ExperimentalStudy
from extra_views import SearchableListMixin


class ExperimentalStudyDetailView(DetailView):
    model = ExperimentalStudy
    template_name = "detail.html"


class ExperimentalStudyListView(SearchableListMixin, ListView):
    model = ExperimentalStudy
    search_fields = ["name"]
    queryset = ExperimentalStudy.objects.order_by("title")
    paginate_by = 100
    template_name = "list.html"
