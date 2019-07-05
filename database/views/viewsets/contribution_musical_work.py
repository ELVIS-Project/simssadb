from database.models import ContributionMusicalWork
from database.serializers import ContributionMusicalWorkSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class ContributionMusicalWorkViewSet(GenericModelViewSet):
    queryset = ContributionMusicalWork.objects.all()
    serializer_class = ContributionMusicalWork
    summary_fields = ["person", "role", "location", "date", "certain"]
    detailed_attributes = [
        "person",
        "role",
        "date",
        "location",
        "contributed_to_work",
    ]
