from database.models.instrument import Instrument
from database.views.viewsets.generic_model_viewset import DetailedAttribute
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class InstrumentViewSet(GenericModelViewSet):
    queryset = Instrument.objects.all().prefetch_related(
            'parts__section__musical_work')
    summary_fields = []
    badge_field = 'musical_works'
    detailed_attributes = [DetailedAttribute(attribute_name='musical_works'),
                           DetailedAttribute(attribute_name='sections'),
                           DetailedAttribute(attribute_name='parts')]
