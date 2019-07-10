from django.views.generic import DetailView
from database.models import Instrument


class InstrumentDetailView(DetailView):
    model = Instrument
    context_object_name = "instrument"
