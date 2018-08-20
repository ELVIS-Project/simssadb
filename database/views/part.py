from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import PartSerializer
from database.models.part import Part
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class PartViewSet(GenericModelViewSet):
    queryset = Part.objects.all().order_by('label')
    serializer_class = PartSerializer


class CreatePartView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = Part
    template_name = 'form.html'