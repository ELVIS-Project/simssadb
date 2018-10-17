from database.models.geographic_area import GeographicArea
from database.serializers import GeographicAreaSerializer
from database.views.generic_model_viewset import DetailedAttribute
from database.views.generic_model_viewset import GenericModelViewSet


class GeographicAreaViewSet(GenericModelViewSet):
    queryset = GeographicArea.objects.all().order_by('name')
    serializer_class = GeographicAreaSerializer
    summary_fields = ['child_areas']
    badge_field = ['musical_works']
    detail_fields = ['part_of',
                     'child_areas',
                     'birth_location_of',
                     'death_location_of',
                     'institutions']
    detailed_attributes = [DetailedAttribute(attribute_name='musical_works',
                                             fields=['composers'],
                                             badge_field='sections'),
                           DetailedAttribute(attribute_name='sections',
                                             fields=['musical_work'],
                                             badge_field='parts'),
                           DetailedAttribute(attribute_name='parts',
                                             fields=['written_for'])]

