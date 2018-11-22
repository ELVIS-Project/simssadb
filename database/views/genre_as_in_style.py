from database.models.genre_as_in_style import GenreAsInStyle
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class CreateGenreAsInStyleView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = GenreAsInStyle
    template_name = 'form.html'