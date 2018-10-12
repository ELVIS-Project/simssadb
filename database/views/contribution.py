from database.models.contribution import Contribution
from database.serializers import ContributionSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class ContributionViewSet(GenericModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer
