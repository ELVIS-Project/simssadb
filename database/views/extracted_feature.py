from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import ExtractedFeatureSerializer
from database.models.extracted_feature import ExtractedFeature


class ExtractedFeatureViewSet(GenericModelViewSet):
    queryset = ExtractedFeature.objects.all()
    serializer_class = ExtractedFeatureSerializer
