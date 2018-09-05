from django.db.models import Count

from database.models.instrument import Instrument
from database.serializers import InstrumentSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class InstrumentViewSet(GenericModelViewSet):
    queryset = Instrument.objects.annotate(
        part_count=Count('part_written_for')).filter(
        part_count__gte=1).prefetch_related('part_written_for',
                                            'part_written_for__in_section'
                                            ).order_by('name')
    serializer_class = InstrumentSerializer
    paginate_by = 100
