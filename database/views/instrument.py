from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import InstrumentSerializer
from database.models.instrument import Instrument


class InstrumentViewSet(GenericModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    paginate_by = 100
