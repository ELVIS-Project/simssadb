from database.models.genre_as_in_type import GenreAsInType
from database.views.generic_model_viewset import GenericModelViewSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class GenreAsInTypeViewSet(GenericModelViewSet):
    queryset = GenreAsInType.objects.all()


class CreateGenreAsInTypeView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = GenreAsInType
    template_name = 'form.html'