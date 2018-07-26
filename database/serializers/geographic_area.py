from rest_framework import serializers
from database.models.geographic_area import GeographicArea


class GeographicAreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GeographicArea
        fields = '__all__'
