from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import SoftwareSerializer
from database.models.software import Software
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class SoftwareViewSet(GenericModelViewSet):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer


class CreateSoftwareView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = Software
    template_name = 'form.html'