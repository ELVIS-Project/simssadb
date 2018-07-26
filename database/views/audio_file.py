from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import AudioFileSerializer
from database.models.audio_file import AudioFile


class AudioFileViewSet(GenericModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
