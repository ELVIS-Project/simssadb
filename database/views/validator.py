from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import ValidatorSerializer
from database.models.validator import Validator


class ValidatorViewSet(GenericModelViewSet):
    queryset = Validator.objects.all()
    serializer_class = ValidatorSerializer
