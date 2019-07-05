from rest_framework import serializers
from database.models.software import Software


class SoftwareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Software
        fields = "__all__"
