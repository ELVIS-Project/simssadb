from rest_framework import serializers
from database.models.musical_work import MusicalWork


class MusicalWorkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MusicalWork
        fields = '__all__'
