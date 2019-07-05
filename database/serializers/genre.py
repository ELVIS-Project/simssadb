from rest_framework import serializers
from database.models.genre_as_in_style import GenreAsInStyle


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenreAsInStyle
        fields = "__all__"
