from database.models.geographic_area import GeographicArea
from database.serializers import GeographicAreaSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)
from database.forms.forms import GeographicAreaForm


class CreateGeographicAreaView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    form_class = GeographicAreaForm
    model = GeographicArea
    template_name = 'form.html'
