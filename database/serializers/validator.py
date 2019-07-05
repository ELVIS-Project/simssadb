from rest_framework import serializers
from database.models.validator import Validator


class ValidatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Validator
        fields = "__all__"
