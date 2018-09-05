from database.models.contributed_to import ContributedTo
from database.serializers import ContributedToSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class ContributedToViewSet(GenericModelViewSet):
    queryset = ContributedTo.objects.all()
    serializer_class = ContributedToSerializer
