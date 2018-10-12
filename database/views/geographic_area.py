from database.models.geographic_area import GeographicArea
from database.serializers import GeographicAreaSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class GeographicAreaViewSet(GenericModelViewSet):
    queryset = GeographicArea.objects.all().order_by('name')
    serializer_class = GeographicAreaSerializer
