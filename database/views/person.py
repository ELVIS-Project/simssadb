from django.db.models import Count

from database.models.person import Person
from database.serializers import PersonSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class PersonViewSet(GenericModelViewSet):
    queryset = Person.objects.annotate(
        work_count=Count('works_contributed_to')).filter(
        work_count__gte=1).prefetch_related('works_contributed_to',
                                            'sections_contributed_to').order_by(
            'surname',
            'given_name')  # only return person with actual musical works
    serializer_class = PersonSerializer
