from rest_framework import serializers
from database.models.symbolic_music_file import SymbolicMusicFile


class SymbolicMusicFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SymbolicMusicFile
        fields = "__all__"
