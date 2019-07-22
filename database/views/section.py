from django.views.generic import DetailView, ListView
from database.models import Section
from extra_views import SearchableListMixin


class SectionDetailView(DetailView):
    model = Section
    context_object_name = "section"


class SectionListView(SearchableListMixin, ListView):
    model = Section
    search_fields = ["title"]
    queryset = Section.objects.order_by("title")
    paginate_by = 100
    template_name = "list.html"
