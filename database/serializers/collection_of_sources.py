from rest_framework import serializers
from database.models.collection_of_sources import CollectionOfSources


class CollectionOfSourcesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CollectionOfSources
        fields = "__all__"
