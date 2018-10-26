from database.models.software import Software
from database.serializers import SoftwareSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class SoftwareViewSet(GenericModelViewSet):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
