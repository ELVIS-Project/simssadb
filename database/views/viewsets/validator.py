from database.models.validator import Validator
from database.serializers import ValidatorSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet
from database.views.viewsets.generic_model_viewset import DetailedAttribute


class ValidatorViewSet(GenericModelViewSet):
    queryset = Validator.objects.all()
    serializer_class = ValidatorSerializer
    detail_fields = ['user',
                     'software',
                     'notes',
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
