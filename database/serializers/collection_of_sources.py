from rest_framework import serializers
from database.models.collection_of_sources import CollectionOfSources


class CollectionOfSourcesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CollectionOfSources
        fields = ('url', 'title', 'editorial_notes', 'publication_date',
                  'person_publisher', 'institution_publisher',
                  'physical_or_electronic')
