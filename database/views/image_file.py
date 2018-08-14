from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import ImageFileSerializer
from database.models.image_file import ImageFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class ImageFileViewSet(GenericModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer


class CreateImageFileView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = ImageFile
    template_name = 'form.html'
