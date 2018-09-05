from database.models.musical_work import MusicalWork
from database.serializers import MusicalWorkSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class MusicalWorkViewSet(GenericModelViewSet):
    queryset = MusicalWork.objects.all().prefetch_related(
            'sections__parts__written_for').order_by(
            'variant_titles')
    serializer_class = MusicalWorkSerializer
