"""Define a CollectionOfSources model"""
from django.contrib.postgres.fields import DateRangeField, IntegerRangeField
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class CollectionOfSources(CustomBaseModel):
    """A reference to one or more Sources grouped together.

    Examples: a book of masses, an album of songs.

    Attributes
    ----------
    CollectionOfSources.title : models.CharField
        The title of this Collection of Sources.

    CollectionOfSources.editorial_notes : models.TextField
        Any editorial notes the user deems necessary.

    CollectionOfSources.date : postgres.fields.DateRangeField
        The date of this Collection of Sources.

    CollectionOfSources.person_publisher : models.ForeignKey
        Reference to the Person that published this Collection of Sources.

    CollectionOfSources.url : models.URLField
        A URL that identifies this Collection of Sources.

    CollectionOfSources.in_archive : models.ManyToManyField
        References to the Archives this Collection of Sources belongs to.

    CollectionOfSources.sources : models.ManyToOneRel
        References to the Sources that are part of this Collection of Sources.

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Sources
    database.models.Person
    database.models.Archive
    """

    title = models.CharField(
        max_length=200, blank=False, help_text="The title of this Collection of Sources"
    )
    editorial_notes = models.TextField(
        blank=True, null=True, help_text="Any editorial notes the user deems necessary"
    )
    date_range_year_only = IntegerRangeField(
        null=True,
        blank=True,
        help_text="The year range of this Collection. If the year is known precisely,"
        " enter only one value. If not, enter a lower and upper bound",
    )
    person_publisher = models.ForeignKey(
        "Person",
        related_name="published",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The Person who published this Collection of Sources",
    )
    url = models.URLField(
        blank=True,
        null=True,
        help_text="An URL that identifies this Collection of Sources",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "collection_of_sources"
        verbose_name_plural = "Collections of Sources"

    def __str__(self):
        return self.title
