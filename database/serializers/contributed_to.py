from rest_framework import serializers
from database.models.contributed_to import ContributedTo


class ContributedToSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContributedTo
        fields = '__all__'
