from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import SymbolicMusicFileSerializer
from database.models.symbolic_music_file import SymbolicMusicFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class SymbolicMusicFileViewSet(GenericModelViewSet):
    queryset = SymbolicMusicFile.objects.all()
    serializer_class = SymbolicMusicFileSerializer


class CreateSymbolicMusicFileView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = SymbolicMusicFile
    template_name = 'form.html'
