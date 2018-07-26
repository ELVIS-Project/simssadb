from rest_framework import serializers
from database.models.section import Section


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
