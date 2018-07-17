from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import SectionSerializer
from database.models.section import Section


class SectionViewSet(GenericModelViewSet):
    queryset = Section.objects.all().prefetch_related('contributed_to', 'contributors',
                                                      'parts', 'parts__written_for')
    serializer_class = SectionSerializer
