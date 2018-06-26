from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import PersonSerializer
from database.models.person import Person
from drf_haystack.viewsets import HaystackViewSet
from database.serializers import PersonSearchSerializer


class PersonViewSet(GenericModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonSearchView(HaystackViewSet):
    index_models = [Person]
    serializer_class = PersonSearchSerializer
