from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import SoftwareSerializer
from database.models.software import Software


class SoftwareViewSet(GenericModelViewSet):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
