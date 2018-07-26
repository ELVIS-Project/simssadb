from rest_framework import serializers
from database.models.text_file import TextFile


class TextFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TextFile
        fields = '__all__'
