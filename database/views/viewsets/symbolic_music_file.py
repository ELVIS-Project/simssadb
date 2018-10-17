from database.models.symbolic_music_file import SymbolicMusicFile
from database.serializers import SymbolicMusicFileSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class SymbolicMusicFileViewSet(GenericModelViewSet):
    queryset = SymbolicMusicFile.objects.all()
    serializer_class = SymbolicMusicFileSerializer
