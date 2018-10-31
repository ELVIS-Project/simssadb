from database.models.research_corpus import ResearchCorpus
from database.serializers import ResearchCorpusSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class ResearchCorpusViewSet(GenericModelViewSet):
    queryset = ResearchCorpus.objects.all()
    serializer_class = ResearchCorpusSerializer
