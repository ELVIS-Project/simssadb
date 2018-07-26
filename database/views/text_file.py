from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import TextFileSerializer
from database.models.text_file import TextFile


class TextFileViewSet(GenericModelViewSet):
    queryset = TextFile.objects.all()
    serializer_class = TextFileSerializer
