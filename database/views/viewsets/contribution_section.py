from database.models import ContributionSection
from database.serializers import ContributionSectionSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class ContributionSectionViewSet(GenericModelViewSet):
    queryset = ContributionSection.objects.all()
    serializer_class = ContributionSectionSerializer
    summary_fields = ["person", "role", "location", "date", "certain"]
    detailed_attributes = [
        "person",
        "role",
        "date",
        "location",
        "contributed_to_work",
    ]
