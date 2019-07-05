from rest_framework import serializers
from database.models.source import Source


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"
