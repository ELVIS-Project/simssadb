from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)
from database.models.section import Section


class CreateSectionView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = Section
    template_name = 'form.html'