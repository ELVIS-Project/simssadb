from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import SourceSerializer
from database.models.source import Source


class SourceViewSet(GenericModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
