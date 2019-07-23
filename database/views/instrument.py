from django.views.generic import DetailView, ListView
from database.models import Instrument
from extra_views import SearchableListMixin

class InstrumentDetailView(DetailView):
    model = Instrument
    context_object_name = "instrument"


class InstrumentListView(SearchableListMixin, ListView):
    model = Instrument
    search_fields = ["name"]
    queryset = Instrument.objects.order_by("name")
    paginate_by = 100
    template_name = "list.html"
