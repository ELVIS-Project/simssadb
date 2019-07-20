from django.views.generic import DetailView, ListView
from database.models import GenreAsInStyle
from extra_views import SearchableListMixin


class GenreAsInStyleDetailView(DetailView):
    model = GenreAsInStyle
    context_object_name = "style"


class GenreAsInStyleListView(SearchableListMixin, ListView):
    model = GenreAsInStyle
    search_fields = ["name"]
    queryset = GenreAsInStyle.objects.order_by("name")
    paginate_by = 100
    template_name = "list.html"
