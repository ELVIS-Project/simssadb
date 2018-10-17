from database.models.genre_as_in_style import GenreAsInStyle
from database.views.generic_model_viewset import GenericModelViewSet
from database.views.generic_model_viewset import DetailedAttribute


class GenreAsInStyleViewSet(GenericModelViewSet):
    queryset = GenreAsInStyle.objects.all()
    badge_field = ['musical_works']
    detailed_attributes = [DetailedAttribute(attribute_name='musical_works',
                                             fields=['composers'],
                                             badge_field='sections')]