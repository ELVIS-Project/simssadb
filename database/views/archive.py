from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import ArchiveSerializer
from database.models.archive import Archive


class ArchiveViewSet(GenericModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer
