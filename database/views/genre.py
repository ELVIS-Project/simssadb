from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import GenreSerializer
from database.models.genre import Genre
from database.forms import GenreForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)

class GenreViewSet(GenericModelViewSet):
    queryset = Genre.objects.all().prefetch_related('style', 'type').order_by('name')
    serializer_class = GenreSerializer


class CreateGenreView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    form_class = GenreForm
    model = Genre