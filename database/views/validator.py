from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import ValidatorSerializer
from database.models.validator import Validator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class ValidatorViewSet(GenericModelViewSet):
    queryset = Validator.objects.all()
    serializer_class = ValidatorSerializer


class CreateValidatorView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = Validator
    template_name = 'form.html'