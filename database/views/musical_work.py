from django.views.generic import DetailView, ListView
from database.models import MusicalWork
from extra_views import SearchableListMixin


class MusicalWorkDetailView(DetailView):
    model = MusicalWork
    context_object_name = "musicalwork"
    queryset = MusicalWork.objects.prefetch_related(
        "parts__written_for", "sections__parts__written_for"
    )


class MusicalWorkListView(SearchableListMixin, ListView):
    model = MusicalWork
    search_fields = [
        "contributions__person__surname",
        "variant_titles",
        "contributions__person__given_name",
    ]
    context_object_name = "musicalworks"
    queryset = MusicalWork.objects.order_by("variant_titles")
    paginate_by = 100
