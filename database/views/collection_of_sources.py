from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import CollectionOfSourcesSerializer
from database.models.collection_of_sources import CollectionOfSources


class CollectionOfSourcesViewSet(GenericModelViewSet):
    queryset = CollectionOfSources.objects.all()
    serializer_class = CollectionOfSourcesSerializer
