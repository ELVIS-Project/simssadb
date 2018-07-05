from drf_haystack.serializers import HaystackSerializerMixin
from rest_framework import serializers
from database.models.source import Source
from rest_framework_recursive.fields import RecursiveField


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        parent_sources = RecursiveField(required=False, allow_null=True,
                                        many=True)
        child_sources = RecursiveField(required=False, allow_null=True,
                                       many=True)
        model = Source
        fields = ('url', 'title', 'languages',
                  'work', 'section', 'part', 'part_of_collection')


class SourceSearchSerializer(HaystackSerializerMixin, SourceSerializer):
    class Meta(SourceSerializer.Meta):
        search_fields = ('text', )
