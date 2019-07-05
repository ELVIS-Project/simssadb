from database.models.source import Source
from database.serializers import SourceSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class SourceViewSet(GenericModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    summary_fields = ["collection", "parent_source", "portion"]
    badge_field = "child_sources"
    detail_fields = ["portion", "collection", "parent_source", "child_sources"]
