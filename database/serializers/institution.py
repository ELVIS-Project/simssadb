from rest_framework import serializers
from database.models.institution import Institution


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
