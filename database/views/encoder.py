from database.models.encoder import Encoder
from database.serializers.encoder import EncoderSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class EncoderViewSet(GenericModelViewSet):
    queryset = Encoder.objects.all()
    serializer_class = EncoderSerializer
