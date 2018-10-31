from database.models.section import Section
from database.serializers import SectionSerializer
from database.views.generic_model_viewset import GenericModelViewSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class SectionViewSet(GenericModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class CreateSectionView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = Section
    template_name = 'form.html'