from database.models.genre_as_in_style import GenreAsInStyle
from database.views.generic_model_viewset import GenericModelViewSet


class GenreAsInStyleViewSet(GenericModelViewSet):
    queryset = GenreAsInStyle.objects.all()
