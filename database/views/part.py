from database.models.part import Part
from database.serializers import PartSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class PartViewSet(GenericModelViewSet):
    queryset = Part.objects.all().order_by('label')
    serializer_class = PartSerializer
