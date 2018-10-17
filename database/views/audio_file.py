from database.models.audio_file import AudioFile
from database.serializers import AudioFileSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class AudioFileViewSet(GenericModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    summary_fields = ['file_type', 'manifests']
    detail_fields = ['encoded_with',
                     'encoding_date',
                     'file_size',
                     'file_type',
                     'extra_metadata',
                     'length',
                     'recording_date',
                     'validated_by',
                     'version',
                     'musical_work',
                     'sections',
                     'parts',
                     'manifests',
                     'file']
