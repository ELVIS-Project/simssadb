from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import ResearchCorpusSerializer
from database.models.research_corpus import ResearchCorpus


class ResearchCorpusViewSet(GenericModelViewSet):
    queryset = ResearchCorpus.objects.all()
    serializer_class = ResearchCorpusSerializer
