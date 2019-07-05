from rest_framework import serializers
from database.models import ContributionMusicalWork


class ContributionMusicalWorkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContributionMusicalWork
        fields = "__all__"
