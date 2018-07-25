from database.views.generic_model_viewset import GenericModelViewSet
from database.models.encoder import Encoder
from rest_framework.serializers import HyperlinkedModelSerializer


class EncoderViewSet(GenericModelViewSet):
    queryset = Encoder.objects.all()
    serializer_class = HyperlinkedModelSerializer
