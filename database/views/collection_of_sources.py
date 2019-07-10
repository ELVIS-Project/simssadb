from django.views.generic import DetailView
from database.models import CollectionOfSources


class CollectionOfSourcesDetailView(DetailView):
    model = CollectionOfSources
    context_object_name = "collection_of_sources"
