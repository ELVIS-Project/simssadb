from rest_framework import serializers
from database.models.research_corpus import ResearchCorpus


class ResearchCorpusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResearchCorpus
        fields = "__all__"
