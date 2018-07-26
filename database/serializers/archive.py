from drf_haystack.serializers import HaystackSerializerMixin
from rest_framework import serializers
from database.models.archive import Archive
from rest_framework_recursive.fields import RecursiveField


class ArchiveSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Archive
        fields = ('url', 'name', 'id', 'collections', 'institution')


class ArchiveSearchSerializer(HaystackSerializerMixin, ArchiveSerializer):
    class Meta(ArchiveSerializer.Meta):
        search_fields = ('text', )
