from rest_framework import serializers
from database.models.person import Person


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('names', 'range_date_birth', 'range_date_death',
                  'birth_location', 'death_location',
                  'viaf_url', 'other_authority_control_url',
                  'works_contributed_to', 'sections_contributed_to',
                  'parts_contributed_to')
