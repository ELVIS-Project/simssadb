from django.views.generic import (CreateView, UpdateView, DeleteView)
from database.models.person import Person
from database.forms.forms import PersonForm
from django.contrib.auth.mixins import LoginRequiredMixin


class CreatePersonView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = PersonForm
    model = Person
    template_name = 'form.html'