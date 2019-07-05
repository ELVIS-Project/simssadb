from database.models.person import Person
from database.serializers import PersonSerializer
from database.views.viewsets.generic_model_viewset import (
    GenericModelViewSet,
    DetailedAttribute,
)


class PersonViewSet(GenericModelViewSet):
    queryset = Person.objects.all().prefetch_related(
        "contributions__contributed_to_work"
    )
    serializer_class = PersonSerializer
    summary_fields = []
    badge_field = "works_composed"
    detail_fields = [
        "birth_location",
        "death_location",
        "date_of_birth",
        "date_of_death",
        "published",
    ]
    detailed_attributes = [
        DetailedAttribute(attribute_name="works_composed"),
        DetailedAttribute(attribute_name="works_arranged"),
        DetailedAttribute(attribute_name="works_authored"),
        DetailedAttribute(attribute_name="works_improvised"),
        DetailedAttribute(attribute_name="works_performed"),
        DetailedAttribute(attribute_name="works_transcribed"),
        DetailedAttribute(attribute_name="sections_composed"),
        DetailedAttribute(attribute_name="sections_arranged"),
        DetailedAttribute(attribute_name="sections_authored"),
        DetailedAttribute(attribute_name="sections_improvised"),
        DetailedAttribute(attribute_name="sections_performed"),
        DetailedAttribute(attribute_name="sections_transcribed"),
        DetailedAttribute(attribute_name="parts_composed"),
        DetailedAttribute(attribute_name="parts_arranged"),
        DetailedAttribute(attribute_name="parts_authored"),
        DetailedAttribute(attribute_name="parts_improvised"),
        DetailedAttribute(attribute_name="parts_performed"),
        DetailedAttribute(attribute_name="parts_transcribed"),
    ]
