from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import ImageFileSerializer
from database.models.image_file import ImageFile


class ImageFileViewSet(GenericModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer
