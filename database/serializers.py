from rest_framework import serializers
import database.models as db


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Instrument
        fields = '__all__'
