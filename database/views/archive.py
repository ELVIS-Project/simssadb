from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers.archive import ArchiveSerializer
from database.models.archive import Archive
from database.forms import ArchiveForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class ArchiveViewSet(GenericModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer


class CreateArchiveView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    form_class = ArchiveForm
    model = Archive
