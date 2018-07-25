from database.views.generic_model_viewset import GenericModelViewSet
from database.models.extracted_feature import ExtractedFeature
from rest_framework.serializers import HyperlinkedModelSerializer


class ExtractedFeaturesViewSet(GenericModelViewSet):
    queryset = ExtractedFeature.objects.all()
    serializer_class = HyperlinkedModelSerializer
