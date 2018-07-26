from rest_framework import serializers
from database.models.archive import Archive


class ArchiveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Archive
        fields = ('name', 'collections', 'institution')
