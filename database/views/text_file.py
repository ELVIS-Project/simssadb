from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import TextFileSerializer
from database.models.text_file import TextFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class TextFileViewSet(GenericModelViewSet):
    queryset = TextFile.objects.all()
    serializer_class = TextFileSerializer


class CreateTextFileView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = TextFile
    template_name = 'form.html'