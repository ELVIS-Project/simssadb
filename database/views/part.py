from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import PartSerializer
from database.models.part import Part


class PartViewSet(GenericModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
