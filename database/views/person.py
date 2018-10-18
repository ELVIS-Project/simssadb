from django.db.models import Count

from database.models.person import Person
from database.serializers import PersonSerializer
from database.views.generic_model_viewset import GenericModelViewSet
from django.views.generic import (CreateView, UpdateView, DeleteView)
from database.models.person import Person
from database.forms.forms import PersonForm
from django.contrib.auth.mixins import LoginRequiredMixin
class PersonViewSet(GenericModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class CreatePersonView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = PersonForm
    model = Person
    template_name = 'form.html'
