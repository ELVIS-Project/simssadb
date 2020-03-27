from django.views.generic import DetailView, ListView
from database.models import ContributionMusicalWork
from extra_views import SearchableListMixin


class ContributionMusicalWorkDetailView(DetailView):
    model = ContributionMusicalWork
    template_name = "detail.html"


class ContributionMusicalWorkListView(SearchableListMixin, ListView):
    model = ContributionMusicalWork
    search_fields = ["role"]
    queryset = ContributionMusicalWork.objects.order_by("id")
    paginate_by = 100
    template_name = "list.html"
