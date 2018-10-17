from database.models.extracted_feature import ExtractedFeature
from database.serializers import ExtractedFeatureSerializer
from database.views.viewsets.generic_model_viewset import DetailedAttribute
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class ExtractedFeatureViewSet(GenericModelViewSet):
    queryset = ExtractedFeature.objects.all()
    serializer_class = ExtractedFeatureSerializer
    summary_fields = []
    detail_fields = ['instance_of_feature',
                     'value',
                     'is_histogram',
                     'code',
                     'group',
                     'feature_of']
    detailed_attributes = [DetailedAttribute(attribute_name='research_corpus',
                                             fields=[],
                                             badge_field='features')]
