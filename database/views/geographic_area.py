from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import GeographicAreaSerializer
from database.models.geographic_area import GeographicArea


class GeographicAreaViewSet(GenericModelViewSet):
    queryset = GeographicArea.objects.all().order_by('name')
    serializer_class = GeographicAreaSerializer
