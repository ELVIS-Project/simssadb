"""Define a Source model"""
from django.db import models
from django.apps import apps
from database.models import CustomBaseModel
from django.db.models import QuerySet
from django.contrib.postgres.fields import IntegerRangeField


class Source(CustomBaseModel):
    """A document containing the music defining a MusicalWork or a
    set of Sections or a set of Parts.

    A Source can be derived from a parent Source, implying a chain of
    provenance.

    Attributes
    ----------
    Source.parent_source : models.ForeignKey
        Reference to the Source this Source was derived from

    Source.child_sources : models.ManyToOneRel
        References to Sources derived from this Source
    """

    title = models.CharField(
        max_length=200, blank=False, help_text="The title of this Source"
    )
    editorial_notes = models.TextField(
        blank=True, null=True, help_text="Any editorial notes the user deems necessary"
    )
    url = models.URLField(
        blank=True, null=True, help_text="An URL that identifies this Source"
    )
    date_range_year_only = IntegerRangeField(
        null=True,
        blank=True,
        help_text="The year range of this Source. If the year is known precisely,"
        " enter only one value. If not, enter a lower and upper bound",
    )
    parent_source = models.OneToOneField(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="child_source",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "source"

    @property
    def files(self) -> QuerySet:
        file_model = apps.get_model("database", "file")
        return file_model.objects.filter(
            id__in=self.source_instantiations.values_list("files", flat=True)
        )
