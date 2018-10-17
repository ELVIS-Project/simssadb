from database.models.encoder import Encoder
from database.serializers.encoder import EncoderSerializer
from database.views.viewsets.generic_model_viewset import DetailedAttribute
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class EncoderViewSet(GenericModelViewSet):
    queryset = Encoder.objects.all()
    serializer_class = EncoderSerializer
    summary_fields = []
    detail_fields = ['user',
                     'software',
                     'notes',
                     'work_flow_file',
                     'work_flow_text']
    detailed_attributes = [DetailedAttribute(attribute_name='audiofile',
                                             fields=['file_type', 'manifests']),
                           DetailedAttribute(attribute_name='imagefile',
                                             fields=['file_type', 'manifests']),
                           DetailedAttribute(
                                   attribute_name='symbolicmusicfile',
                                   fields=['file_type', 'manifests']),
                           DetailedAttribute(attribute_name='textfile',
                                             fields=['file_type', 'manifests'])]
