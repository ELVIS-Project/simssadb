from database.models.instrument import Instrument
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class InstrumentViewSet(GenericModelViewSet):
    queryset = Instrument.objects.all()
