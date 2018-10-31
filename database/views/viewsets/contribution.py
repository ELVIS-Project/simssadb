from database.models.contribution import Contribution
from database.serializers import ContributionSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class ContributionViewSet(GenericModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer
    summary_fields = ['person', 'role', 'location', 'date', 'certain']
    detailed_attributes = ['person',
                           'role',
                           'date',
                           'location',
                           'contributed_to_part',
                           'contributed_to_section',
                           'contributed_to_work']
