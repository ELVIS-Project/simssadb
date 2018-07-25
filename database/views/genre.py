from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import GenreSerializer
from database.models.genre import Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from database.forms import GenreForm
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)


class GenreViewSet(GenericModelViewSet):
    queryset = Genre.objects.all().prefetch_related('style', 'type').order_by('name')
    serializer_class = GenreSerializer


class CreateGenreView(LoginRequiredMixin,CreateView): # This function searches for post_form page!
    # you cannot create a post unless logged in
    login_url = '/login/'
    redirect_field_name = 'home.html'  # save the new post, and it redirects to post_detail page

    form_class = GenreForm  # This creates a new PostForm, and PostForm already specifies which fields we need to create
    model = Genre