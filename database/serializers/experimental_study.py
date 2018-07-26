from rest_framework import serializers
from database.models.experimental_study import ExperimentalStudy


class ExperimentalStudySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExperimentalStudy
        fields = '__all__'
