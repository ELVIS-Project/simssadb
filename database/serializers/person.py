from rest_framework import serializers
from database.models.person import Person


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"
