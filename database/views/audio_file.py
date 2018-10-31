from database.models.audio_file import AudioFile
from database.serializers import AudioFileSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class AudioFileViewSet(GenericModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
