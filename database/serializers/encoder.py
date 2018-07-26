from rest_framework import serializers
from database.models.encoder import Encoder


class EncoderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Encoder
        fields = '__all__'
