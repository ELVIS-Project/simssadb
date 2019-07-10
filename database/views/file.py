from django.views.generic import DetailView
from database.models import File


class FileDetailView(DetailView):
    model = File
    context_object_name = "file"
