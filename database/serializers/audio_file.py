from rest_framework import serializers
from database.models.audio_file import AudioFile


class AudioFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AudioFile
        fields = '__all__'
