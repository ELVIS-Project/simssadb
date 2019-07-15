from django.views.generic import DetailView
from database.models import MusicalWork
from typing import Dict
from django.urls import reverse
from django.db.models import F


class MusicalWorkDetailView(DetailView):
    model = MusicalWork
    context_object_name = "musicalwork"
    queryset = MusicalWork.objects.prefetch_related(
        "parts__written_for", "sections__parts__written_for",
    )
