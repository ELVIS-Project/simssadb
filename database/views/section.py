from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import SectionSerializer
from database.models.section import Section


class SectionViewSet(GenericModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

