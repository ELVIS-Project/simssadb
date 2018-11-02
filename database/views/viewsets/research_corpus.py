from database.models.research_corpus import ResearchCorpus
from database.serializers import ResearchCorpusSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet
from database.views.viewsets.generic_model_viewset import DetailedAttribute


class ResearchCorpusViewSet(GenericModelViewSet):
    queryset = ResearchCorpus.objects.all().\
        prefetch_related('features__instance_of_feature',
                         'files__manifests__source',
                         'features__feature_of')
    serializer_class = ResearchCorpusSerializer
    summary_fields = ['creators', 'curators']
    badge_field = 'files'
    detail_fields = ['creators', 'curators']
    detailed_attributes = [DetailedAttribute(attribute_name='files',
                                             fields=['file_type',
                                                     'file_size',
                                                     'source']),
                           DetailedAttribute(attribute_name='features',
                                             fields=['feature_of'])]
