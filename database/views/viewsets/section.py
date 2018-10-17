from database.models.section import Section
from database.serializers import SectionSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class SectionViewSet(GenericModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
