from database.models.text_file import TextFile
from database.serializers import TextFileSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class TextFileViewSet(GenericModelViewSet):
    queryset = TextFile.objects.all()
    serializer_class = TextFileSerializer
    summary_fields = ["musical_work", "file_type", "file_size", "source"]
    detail_fields = [
        "encoded_with",
        "encoding_date",
        "file_size",
        "file_type",
        "extra_metadata",
        "validated_by",
        "version",
        "musical_work",
        "sections",
        "parts",
        "source",
        "file",
    ]
