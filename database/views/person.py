from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import PersonSerializer
from database.models.person import Person


class PersonViewSet(GenericModelViewSet):
    queryset = Person.objects.all().prefetch_related('works_contributed_to',
                                                     'sections_contributed_to').order_by('surname', 'given_name')
    serializer_class = PersonSerializer

