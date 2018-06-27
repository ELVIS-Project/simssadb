from drf_haystack.serializers import HaystackSerializerMixin
from rest_framework import serializers
from database.models.genre import Genre


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('url', 'name', 'id')


class GenreSearchSerializer(HaystackSerializerMixin, GenreSerializer):
    class Meta(GenreSerializer.Meta):
        search_fields = ('text', )
