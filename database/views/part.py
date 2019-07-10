from django.views.generic import DetailView
from database.models import Part


class PartDetailView(DetailView):
    model = Part
    context_object_name = "part"
