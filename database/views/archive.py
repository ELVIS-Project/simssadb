from database.models.archive import Archive
from database.serializers import ArchiveSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class ArchiveViewSet(GenericModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer
