from django.views.generic import DetailView
from database.models import Section


class SectionDetailView(DetailView):
    model = Section
    context_object_name = "section"
