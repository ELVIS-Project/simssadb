from django.views.generic import DetailView
from database.models import GenreAsInStyle


class GenreAsInStyleDetailView(DetailView):
    model = GenreAsInStyle
    context_object_name = "style"
