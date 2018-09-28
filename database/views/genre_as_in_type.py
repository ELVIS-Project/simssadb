from database.models.genre_as_in_type import GenreAsInType
from database.views.generic_model_viewset import GenericModelViewSet


class GenreAsInTypeViewSet(GenericModelViewSet):
    queryset = GenreAsInType.objects.all()
