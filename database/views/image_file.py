from database.models.image_file import ImageFile
from database.serializers import ImageFileSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class ImageFileViewSet(GenericModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer
