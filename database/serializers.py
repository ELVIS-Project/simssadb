from rest_framework import serializers
from database.models import *
from rest_framework_recursive.fields import RecursiveField


class InstrumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instrument
        fields = ('url', 'name', 'id')


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('url', 'name', 'id')


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('names', 'range_date_birth', 'range_date_death',
                  'birth_location', 'death_location',
                  'viaf_url', 'other_authority_control_url')


class GeographicAreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GeographicArea
        fields = ('url', 'name', 'id', 'part_of')


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    parents = RecursiveField(required=False, allow_null=True, many=True)
    children = RecursiveField(required=False, allow_null=True, many=True)

    class Meta:
        model = Section
        fields = ('url', 'title', 'id', 'parts', 'ordering',
                  'contributors', 'parents', 'children')
