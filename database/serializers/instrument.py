from rest_framework import serializers
from database.models.instrument import Instrument


class InstrumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instrument
        fields = '__all__'
