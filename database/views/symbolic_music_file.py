from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import SymbolicMusicFileSerializer
from database.models.symbolic_music_file import SymbolicMusicFile


class SymbolicMusicFileViewSet(GenericModelViewSet):
    queryset = SymbolicMusicFile.objects.all()
    serializer_class = SymbolicMusicFileSerializer
