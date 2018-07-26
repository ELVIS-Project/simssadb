from rest_framework import serializers
from database.models.image_file import ImageFile


class ImageFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImageFile
        fields = '__all__'
