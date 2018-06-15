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
