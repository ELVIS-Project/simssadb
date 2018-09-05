from database.models.source import Source
from database.serializers import SourceSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class SourceViewSet(GenericModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
