from database.models.musical_work import MusicalWork
from database.serializers import MusicalWorkSerializer
from database.views.viewsets.generic_model_viewset import DetailedAttribute, \
    GenericModelViewSet


class MusicalWorkViewSet(GenericModelViewSet):
    queryset = MusicalWork.objects.all().prefetch_related(
            'sections__parts__written_for').order_by(
            'variant_titles')
    serializer_class = MusicalWorkSerializer
    summary_fields = ['composers']
    badge_field = 'sections'
    detail_fields = ['variant_titles',
                     'genres_as_in_style',
                     'genres_as_in_type',
                     'certainty_of_attributions',
                     'sacred_or_secular',
                     'collections_of_sources',
                     'instrumentation',
                     'contributions',
                     'languages']
    detailed_attributes = [DetailedAttribute(attribute_name='sections',
                                             fields=['child_sections',
                                                     'parent_sections'],
                                             badge_field='parts')]
