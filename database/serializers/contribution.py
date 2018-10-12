from rest_framework import serializers
from database.models.contribution import Contribution


class ContributionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contribution
        fields = '__all__'
