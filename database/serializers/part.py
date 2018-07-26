from rest_framework import serializers
from database.models.part import Part


class PartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Part
        fields = ('url', 'label', 'written_for', 'contributors')
