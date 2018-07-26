from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import MusicalWorkSerializer
from database.models.musical_work import MusicalWork
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)
from database.forms import MusicalWorkForm


class MusicalWorkViewSet(GenericModelViewSet):
    queryset = MusicalWork.objects.all().prefetch_related('sections').order_by('variant_titles')
    serializer_class = MusicalWorkSerializer


class CreateMusicalWorkView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    form_class = MusicalWorkForm
    model = MusicalWork