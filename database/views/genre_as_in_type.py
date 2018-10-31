from database.models.genre_as_in_type import GenreAsInType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class CreateGenreAsInTypeView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = GenreAsInType
    template_name = 'form.html'