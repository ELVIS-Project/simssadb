from rest_framework import serializers
from database.models import *


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
