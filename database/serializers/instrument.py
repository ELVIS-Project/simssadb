from drf_haystack.serializers import HaystackSerializerMixin
from rest_framework import serializers
from database.models.instrument import Instrument


class InstrumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instrument
        fields = ('url', 'name', 'id')


class InstrumentSearchSerializer(HaystackSerializerMixin, InstrumentSerializer):
    class Meta(InstrumentSerializer.Meta):
        search_fields = ('text', )
