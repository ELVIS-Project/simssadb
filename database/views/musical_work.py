from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import MusicalWorkSerializer
from database.models.musical_work import MusicalWork


class MusicalWorkViewSet(GenericModelViewSet):
    queryset = MusicalWork.objects.all().prefetch_related('sources', 'genres_as_in_style',
                                                          'genres_as_in_type', 'sections__parts', 'sections__in_works',
                                                          'sections__contributed_to__person')
    serializer_class = MusicalWorkSerializer
