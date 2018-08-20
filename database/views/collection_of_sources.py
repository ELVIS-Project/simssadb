from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import CollectionOfSourcesSerializer
from database.models.collection_of_sources import CollectionOfSources
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)

class CollectionOfSourcesViewSet(GenericModelViewSet):
    queryset = CollectionOfSources.objects.all().order_by('title')
    serializer_class = CollectionOfSourcesSerializer


class CreateCollectionOfSourcesView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = CollectionOfSources
    fields = '__all__'
    template_name = 'form.html'