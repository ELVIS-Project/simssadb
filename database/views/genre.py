from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import GenreSerializer
from database.models.genre import Genre


class GenreViewSet(GenericModelViewSet):
    queryset = Genre.objects.all().prefetch_related('style', 'type').order_by('name')
    serializer_class = GenreSerializer
