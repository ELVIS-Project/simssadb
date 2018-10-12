from database.models.musical_work import MusicalWork
from database.serializers import MusicalWorkSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class MusicalWorkViewSet(GenericModelViewSet):
    queryset = MusicalWork.objects.all().prefetch_related(
            'sections__parts__written_for').order_by(
            'variant_titles')
    serializer_class = MusicalWorkSerializer
    summary_fields = ['composers']
    detail_fields = ['variant_titles',
                     'genres_as_in_style',
                     'genres_as_in_type',
                     'certainty_of_attributions',
                     'sacred_or_secular',
                     'collections_of_sources',
                     'instrumentation',
                     'contributions',
                     'languages']
    related_fields = [{
        'object_name': 'sections',
        'fields':      ['parent_sections', 'child_sections'],
        'badge':       'parts'
        }]
