from database.models.validator import Validator
from database.serializers import ValidatorSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class ValidatorViewSet(GenericModelViewSet):
    queryset = Validator.objects.all()
    serializer_class = ValidatorSerializer
