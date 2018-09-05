from database.models.text_file import TextFile
from database.serializers import TextFileSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class TextFileViewSet(GenericModelViewSet):
    queryset = TextFile.objects.all()
    serializer_class = TextFileSerializer
