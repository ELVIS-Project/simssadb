from database.models.section import Section
from database.serializers import SectionSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class SectionViewSet(GenericModelViewSet):
    queryset = Section.objects.all().prefetch_related('parts',
                                                      'in_works').order_by(
        'title')
    serializer_class = SectionSerializer
