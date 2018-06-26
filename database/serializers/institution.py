from rest_framework import serializers
from database.models.institution import Institution
from drf_haystack.serializers import HaystackSerializerMixin


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = ('url', 'name', 'located_at', 'website')


class InstitutionSearchSerializer(HaystackSerializerMixin, InstitutionSerializer):
    class Meta(InstitutionSerializer.Meta):
        search_fields = ('text', )
