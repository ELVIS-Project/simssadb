from rest_framework import serializers
from database.models.extracted_feature import ExtractedFeature


class ExtractedFeatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExtractedFeature
        fields = '__all__'
