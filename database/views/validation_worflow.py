from django.views.generic import DetailView, ListView
from database.models import ValidationWorkFlow
from extra_views import SearchableListMixin


class ValidationWorkFlowDetailView(DetailView):
    model = ValidationWorkFlow
    template_name = "detail.html"


class ValidationWorkFlowListView(SearchableListMixin, ListView):
    model = ValidationWorkFlow
    search_fields = ["validator_names"]
    queryset = ValidationWorkFlow.objects.order_by("validator_names")
    paginate_by = 100
    template_name = "list.html"
