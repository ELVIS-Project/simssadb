from database.models.archive import Archive
from database.serializers import ArchiveSerializer
from database.views.viewsets.generic_model_viewset import (
    GenericModelViewSet,
    DetailedAttribute,
)


class ArchiveViewSet(GenericModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer
    detail_fields = ["institution"]
    summary_fields = ["institution"]
    badge_field = ["collections"]
    detailed_attributes = [
        DetailedAttribute(
            attribute_name="collections", fields=[], badge_field="sources"
        )
    ]
