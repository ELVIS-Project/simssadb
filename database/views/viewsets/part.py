from django.db.models import Prefetch

from database.models.part import Part
from database.serializers import PartSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet


class PartViewSet(GenericModelViewSet):
    queryset = Part.objects.all().prefetch_related(
        "section__musical_work", "written_for", "source_instantiations"
    )
    serializer_class = PartSerializer
    summary_fields = ["section"]
    badge_field = "symbolic_files"
    detail_fields = [
        "written_for",
        "contributions",
        "certainty_of_attributions",
        "collections_of_sources",
        "written_for",
    ]
