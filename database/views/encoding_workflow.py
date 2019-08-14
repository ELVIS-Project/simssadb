from django.views.generic import DetailView, ListView
from database.models import EncodingWorkFlow
from extra_views import SearchableListMixin


class EncodingWorkflowDetailView(DetailView):
    model = EncodingWorkFlow
    template_name = "detail.html"


class EncodingWorkflowListView(SearchableListMixin, ListView):
    model = EncodingWorkFlow
    search_fields = ["name"]
    queryset = EncodingWorkFlow.objects.order_by("name")
    paginate_by = 100
    template_name = "list.html"
