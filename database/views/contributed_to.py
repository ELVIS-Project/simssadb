from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import ContributedToSerializer
from database.models.contributed_to import ContributedTo


class ContributedToViewSet(GenericModelViewSet):
    queryset = ContributedTo.objects.all()
    serializer_class = ContributedToSerializer
