from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import InstrumentSerializer
from database.models.instrument import Instrument
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)
from database.forms import InstrumentForm

class InstrumentViewSet(GenericModelViewSet):
    queryset = Instrument.objects.all().prefetch_related('part_written_for',
                                                         'part_written_for__in_section').order_by('name')
    serializer_class = InstrumentSerializer
    paginate_by = 100


class CreateInstrumentView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    form_class = InstrumentForm
    model = Instrument
