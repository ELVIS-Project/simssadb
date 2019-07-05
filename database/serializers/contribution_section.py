from rest_framework import serializers
from database.models import ContributionSection


class ContributionSectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContributionSection
        fields = "__all__"
