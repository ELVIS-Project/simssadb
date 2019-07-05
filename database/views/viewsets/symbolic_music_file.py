from database.models.symbolic_music_file import SymbolicMusicFile
from database.serializers import SymbolicMusicFileSerializer
from database.views.viewsets.generic_model_viewset import DetailedAttribute
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class SymbolicMusicFileViewSet(GenericModelViewSet):
    queryset = SymbolicMusicFile.objects.all()
    serializer_class = SymbolicMusicFileSerializer
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
        "feature_files",
    ]
    detailed_attributes = [
        DetailedAttribute(attribute_name="one_dimensional_features", fields=[]),
        DetailedAttribute(attribute_name="histograms", fields=[]),
    ]
