from database.models.institution import Institution
from database.serializers import InstitutionSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class InstitutionViewSet(GenericModelViewSet):
    queryset = Institution.objects.all().order_by('name')
    serializer_class = InstitutionSerializer
