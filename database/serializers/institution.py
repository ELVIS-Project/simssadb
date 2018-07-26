from rest_framework import serializers
from database.models.institution import Institution


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = ('url', 'name', 'located_at', 'website')
