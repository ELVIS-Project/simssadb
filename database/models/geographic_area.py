"""Define a GeographicArea model"""
from django.apps import apps
from django.db import models
from django.db.models import QuerySet

from database.models.custom_base_model import CustomBaseModel


class GeographicArea(CustomBaseModel):
    """A geographic area that can be part of another area

    Attributes
    ----------
    name : models.CharField
        The name of this GeographicArea

    authority_control_url : models.URLField
        An URL linking to an authority control description of this GeographicArea

    part_of : models.ForeignKey
        The parent area of this GeographicArea (e.g. Montreal has Quebec as
        parent area)

    child_areas : model.fields.related_descriptors.ReverseManyToOneDescriptor
        References to the child areas of this GeographicArea

    birth_location_of : models.fields.related_descriptors.ReverseManyToOneDescriptor
        References to Persons that were born in this GeographicArea

    death_location_of : models.fields.related_descriptors.ReverseManyToOneDescriptor
        References to Persons that died in this GeographicArea

    contributions : models.fields.related_descriptors.ReverseManyToOneDescriptor
        References to the Contributions made in this GeographicArea
    """

    name = models.CharField(max_length=200, help_text="The name of the Geographic Area")
    part_of = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text='The "parent area" of this '
        "Geographic Area. "
        "Example: Montreal has as "
        "parent area Quebec",
        related_name="child_areas",
    )
    authority_control_url = models.URLField(
        blank=True,
        null=True,
        help_text="An URI linking to an "
        "authority control "
        "description of this "
        "Geographic Area",
    )

    class Meta:
        db_table = "geographic_area"
        verbose_name_plural = "Geographic Areas"

    def __str__(self):
        return self.name

    @property
    def musical_works(self) -> QuerySet:
        """Get the MusicalWorks that have contributions made in this area."""
        work_model = apps.get_model("database", "musicalwork")
        work_ids = set()
        for contribution in self.contributionmusicalwork_set.all():
            work_ids.add(contribution.contributed_to_work_id)
        return work_model.objects.filter(id__in=work_ids)
