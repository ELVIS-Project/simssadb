from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializerMixin
from database.models.geographic_area import GeographicArea


class GeographicAreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GeographicArea
        fields = ('url', 'name', 'id', 'part_of')


class GeographicAreaSearchSerializer(HaystackSerializerMixin,
                                     GeographicAreaSerializer):
    class Meta(GeographicAreaSerializer.Meta):
        search_fields = ('text', )