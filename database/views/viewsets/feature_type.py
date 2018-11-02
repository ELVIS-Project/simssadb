from database.models.feature_type import FeatureType
from database.serializers import ExtractedFeatureSerializer
from database.views.viewsets.generic_model_viewset import DetailedAttribute
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class FeatureTypeViewSet(GenericModelViewSet):
    queryset = FeatureType.objects.all().\
        prefetch_related('instances__feature_of')
    serializer_class = ExtractedFeatureSerializer
    summary_fields = []
    detail_fields = ['code', 'description', 'is_sequential', 'dimensions',
                     'min_val', 'max_val']
    detailed_attributes = [DetailedAttribute(attribute_name='instances',
                                             fields=['feature_of'])]
