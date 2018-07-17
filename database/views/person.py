from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import PersonSerializer
from database.models.person import Person
from drf_haystack.viewsets import HaystackViewSet
from database.serializers import PersonSearchSerializer


class PersonViewSet(GenericModelViewSet):
    queryset = Person.objects.all().prefetch_related('birth_location', 'death_location',
                                                     'contributed_to', 'contributed_to__contributed_to_work',
                                                     'contributed_to__contributed_to_part',
                                                     'contributed_to__contributed_to_section',
                                                     'parts_contributed_to',
                                                     'sections_contributed_to', 'works_contributed_to')
    serializer_class = PersonSerializer


class PersonSearchView(HaystackViewSet):
    index_models = [Person]
    serializer_class = PersonSearchSerializer
