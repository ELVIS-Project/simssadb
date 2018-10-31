from database.models.extracted_feature import ExtractedFeature
from database.serializers import ExtractedFeatureSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class ExtractedFeatureViewSet(GenericModelViewSet):
    queryset = ExtractedFeature.objects.all()
    serializer_class = ExtractedFeatureSerializer
