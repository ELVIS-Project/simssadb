from database.models.genre_as_in_type import GenreAsInType
from database.views.viewsets.generic_model_viewset import DetailedAttribute
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class GenreAsInTypeViewSet(GenericModelViewSet):
    queryset = GenreAsInType.objects.all()
    badge_field = ['musical_works']
    detailed_attributes = [DetailedAttribute(attribute_name='musical_works',
                                             fields=['composers'],
                                             badge_field='sections')]
