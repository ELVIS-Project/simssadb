from drf_haystack.serializers import HaystackSerializerMixin
from rest_framework import serializers
from database.models.section import Section
from rest_framework_recursive.fields import RecursiveField


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    parents = RecursiveField(required=False, allow_null=True, many=True)
    children = RecursiveField(required=False, allow_null=True, many=True)

    class Meta:
        model = Section
        fields = ('url', 'title', 'id', 'parts', 'ordering',
                  'contributors', 'parents', 'children', 'in_works')


class SectionSearchSerializer(HaystackSerializerMixin, SectionSerializer):
    class Meta(SectionSerializer.Meta):
        search_fields = ('text', )
