"""Define a Source model"""
from django.db import models
from django.db.models import CheckConstraint, Q
from django.apps import apps
from database.models import CustomBaseModel
from psycopg2.extras import NumericRange
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

    TYPES = (("MANUSCRIPT", "Manuscript"), ("PRINT", "Print"), ("DIGITAL", "Digital"))
    title = models.CharField(
        max_length=200, null=False, blank=False, help_text="The title of this Source"
    )
    source_type = models.CharField(
        default="PRINT",
        max_length=30,
        choices=TYPES,
        help_text="The type of this Source",
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
    language_of_text = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="The language of the text of this Source",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "source"
        constraints = [
            CheckConstraint(
                check=(
                    (
                        Q(date_range_year_only__startswith__isnull=False)
                        & Q(date_range_year_only__endswith__isnull=False)
                    )
                    | Q(date_range_year_only__isnull=True)
                ),
                name="source_date_range_bounds_not_null",
            )
        ]

    def clean(self) -> None:
        if self.date_range_year_only:
            if (
                self.date_range_year_only.lower is None
                and self.date_range_year_only.upper is not None
            ):
                self.date_range_year_only = NumericRange(
                    self.date_range_year_only.upper,
                    self.date_range_year_only.upper,
                    bounds="[]",
                )
            elif (
                self.date_range_year_only.lower is not None
                and self.date_range_year_only.upper is None
            ):
                self.date_range_year_only = NumericRange(
                    self.date_range_year_only.lower,
                    self.date_range_year_only.lower,
                    bounds="[]",
                )
            else:
                self.date_range_year_only = NumericRange(
                    self.date_range_year_only.lower,
                    self.date_range_year_only.upper,
                    bounds="[]",
                )

    @property
    def files(self) -> QuerySet:
        file_model = apps.get_model("database", "file")
        return file_model.objects.filter(
            id__in=self.source_instantiations.values_list("files", flat=True)
        )
