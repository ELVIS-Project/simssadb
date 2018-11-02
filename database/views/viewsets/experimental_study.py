from database.models.experimental_study import ExperimentalStudy
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class ExperimentalStudyViewSet(GenericModelViewSet):
    queryset = ExperimentalStudy.objects.all()
    detail_fields = ['published', 'date', 'link', 'research_corpus_used',
                     'institution', 'authors']
    summary_fields = ['authors']
