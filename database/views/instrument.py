from django.db.models import Count

from database.models.instrument import Instrument
from database.serializers import InstrumentSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class InstrumentViewSet(GenericModelViewSet):
    queryset = Instrument.objects.all()
