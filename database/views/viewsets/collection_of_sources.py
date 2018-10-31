from database.models.collection_of_sources import CollectionOfSources
from database.serializers import CollectionOfSourcesSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet, \
    DetailedAttribute


class CollectionOfSourcesViewSet(GenericModelViewSet):
    queryset = CollectionOfSources.objects.all().order_by('title')
    serializer_class = CollectionOfSourcesSerializer
    summary_fields = ['in_archive']
    badge_field = ['sources']
    detail_fields = ['in_archive',
                     'institution_publisher',
                     'person_publisher',
                     'editorial_notes']
    detailed_attributes = [DetailedAttribute(attribute_name='sources',
                                             fields=['parent_sources',
                                                     'child_sources'
                                                     'portion'])]
