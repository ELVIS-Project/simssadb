from rest_framework import serializers
from database.models.geographic_area import GeographicArea


class GeographicAreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GeographicArea
        fields = ('url', 'name', 'id', 'part_of')
