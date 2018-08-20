from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import GenreSerializer
from database.models.genre import Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)
from django.db.models import Count


class GenreViewSet(GenericModelViewSet):
    queryset = Genre.objects.annotate(work_count=Count('style') + Count('type')).filter(work_count__gte=1).\
        prefetch_related('style', 'type').order_by('name')
    serializer_class = GenreSerializer


class CreateGenreView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = Genre
    template_name = 'form.html'
