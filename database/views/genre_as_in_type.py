from django.views.generic import DetailView
from database.models import GenreAsInType


class GenreAsInTypeDetailView(DetailView):
    model = GenreAsInType
    context_object_name = "type"
