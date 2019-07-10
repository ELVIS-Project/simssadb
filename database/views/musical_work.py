from django.views.generic import DetailView
from database.models import MusicalWork
from typing import Dict


class MusicalWorkDetailView(DetailView):
    model = MusicalWork
    context_object_name = "musicalwork"
    queryset = MusicalWork.objects.prefetch_related(
        "genres_as_in_style",
        "genres_as_in_type",
        "sections__parts",
        "parts__written_for",
    )
