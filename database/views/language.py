from django.views.generic import DetailView, ListView
from database.models import Language
from extra_views import SearchableListMixin


class LanguageDetailView(DetailView):
    model = Language
    template_name = "detail.html"


class LanguageListView(SearchableListMixin, ListView):
    model = Language
    search_fields = ["name"]
    queryset = Language.objects.order_by("name")
    paginate_by = 100
    template_name = "list.html"
