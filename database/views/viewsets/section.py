from database.models.section import Section
from database.serializers import SectionSerializer
from database.views.viewsets.generic_model_viewset import GenericModelViewSet
from database.views.viewsets.generic_model_viewset import DetailedAttribute

class SectionViewSet(GenericModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    detail_fields = ['certainty_of_attributions',
                     'sacred_or_secular',
                     'collections_of_sources',
                     'instrumentation',
                     'contributions',
                     'languages',
                     'musical_work']
    detailed_attributes = [DetailedAttribute(attribute_name='child_sections'),
                           DetailedAttribute(attribute_name='parent_sections')]
