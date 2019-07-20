from django.views.generic import DetailView, ListView
from database.models import GenreAsInType
from extra_views import SearchableListMixin


class GenreAsInTypeDetailView(DetailView):
    model = GenreAsInType
    context_object_name = "type"


class GenreAsInTypeListView(SearchableListMixin, ListView):
    model = GenreAsInType
    search_fields = ["name"]
    queryset = GenreAsInType.objects.order_by("name")
    paginate_by = 100
    template_name = "list.html"
