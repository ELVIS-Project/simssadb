from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import InstitutionSerializer
from database.models.institution import Institution
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class InstitutionViewSet(GenericModelViewSet):
    queryset = Institution.objects.all().order_by('name')
    serializer_class = InstitutionSerializer


class CreateInstitutionView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Institution
    fields = '__all__'
    template_name = 'form.html'