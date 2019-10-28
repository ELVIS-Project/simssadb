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
    parent_source : models.OneToOneField
        Reference to the Source this Source was derived from

    child_source : models.fields.related_descriptors.ReverseOneToOneDescriptor
        Reference to a child Source derived from this Source

    title : models.CharField
        The title of this Source
    
    editorial_notes : models.TextField
        Any editorial notes the user deems necessary to add
    
    url : models.URLField
        An URL that identifies this Source
    
    source_type : models.CharField
        The type of this source. Can be one of Manuscript, Print or Digital
    
    language_of_text : models.CharField
        The language of the text of this Source
    
    in_archive : models.fields.related_descriptors.ManyToManyDescriptor
        References to Archives that contain this Source

    source_instantiations : models.fields.related_descriptors.ReverseManyToOneDescriptor
        References to Source Instantiations related to this Source

     date_range_year_only: IntegerRangeField
        An integer range representing an year range that this Source was published.
        
        An integer range is used to allow for uncertain dates. The range thus represents
        a lower and upper bound on the years that this Source could possibly have been
        published.
        
        Ranges in PostgreSQL are standardized to a ``[)`` interval, that is closed on 
        the lower bound and open on the upper bound. 

        If the date of the Source can be determined to one specific year, then 
        such year should be entered as the lower bound and the next year as the upper 
        bound (since the upper bound is open). For example, if the year is determined to 
        be 1750, the range should then be ``[1750, 1751)``.

        If the Contribution could have occurred between the years of 1749 and 1755, then
        the range should be ``[1749, 1756)`` to account for the open upper bound.

        Neither bound should be ``Null`` since PostgreSQL interprets those as infinity.
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
        verbose_name_plural = "Sources"
        constraints = [
            CheckConstraint(
                # Checks that the date_range_year_only field either has both bounds
                # filled or it is null
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
        #TODO: refactor
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

    def __str__(self):
        return self.title

    @property
    def files(self) -> QuerySet:
        """Gets all the Files related to this Source through a Source Instantiation
        
        Returns
        -------
        QuerySet
            A QuerySet of Files related to this Source
        """
        file_model = apps.get_model("database", "file")
        return file_model.objects.filter(
            id__in=self.source_instantiations.values_list("files", flat=True)
        )
