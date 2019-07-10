from django.views.generic import DetailView
from database.models import Source


class SourceDetailView(DetailView):
    model = Source
    context_object_name = "source"
