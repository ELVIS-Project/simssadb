from database.models.person import Person
from database.serializers import PersonSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class PersonViewSet(GenericModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
