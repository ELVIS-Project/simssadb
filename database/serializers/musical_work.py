from rest_framework import serializers
from database.models.musical_work import MusicalWork


class MusicalWorkSerializer(serializers.HyperlinkedModelSerializer):
    composers = serializers.HyperlinkedRelatedField(
            many=True,
            read_only=True,
            view_name='person-detail'
    )

    class Meta:
        model = MusicalWork
        fields = ('url', 'variant_titles', 'genres_as_in_style',
                  'genres_as_in_form',
                  'sections', 'religiosity', 'viaf_url',
                  'other_authority_control_url', 'contributors',
                  'composers')
