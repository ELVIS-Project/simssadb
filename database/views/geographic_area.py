from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import GeographicAreaSerializer
from database.models.geographic_area import GeographicArea
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)
from database.forms import GeographicAreaForm

class GeographicAreaViewSet(GenericModelViewSet):
    queryset = GeographicArea.objects.all().order_by('name')
    serializer_class = GeographicAreaSerializer


class CreateGeographicAreaView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    form_class = GeographicAreaForm
    model = GeographicArea
    template_name = 'form.html'