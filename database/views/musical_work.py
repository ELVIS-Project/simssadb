from database.models.musical_work import MusicalWork
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)
from database.forms.forms import MusicalWorkForm


class CreateMusicalWorkView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = MusicalWorkForm
    model = MusicalWork
    template_name = 'form.html'
