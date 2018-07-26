from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import AudioFileSerializer
from database.models.audio_file import AudioFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class AudioFileViewSet(GenericModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer


class CreateAudioFileView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = AudioFile
