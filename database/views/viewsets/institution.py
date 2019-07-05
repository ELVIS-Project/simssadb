from database.models.institution import Institution
from database.serializers import InstitutionSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet
from database.views.viewsets.generic_model_viewset import DetailedAttribute


class InstitutionViewSet(GenericModelViewSet):
    queryset = Institution.objects.all().order_by("name")
    serializer_class = InstitutionSerializer
    detail_fields = ["located_at", "website"]
    detailed_attributes = [
        DetailedAttribute(attribute_name="archives"),
        DetailedAttribute(attribute_name="published"),
        DetailedAttribute(attribute_name="studies"),
    ]
