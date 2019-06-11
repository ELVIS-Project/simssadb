"""Define a MusicalWork model"""
from django.apps import apps
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models import QuerySet

from database.mixins.contribution_info_mixin import ContributionInfoMixin
from database.mixins.file_and_source_info_mixin import FileAndSourceInfoMixin
from database.models.custom_base_model import CustomBaseModel


class MusicalWork(FileAndSourceInfoMixin, ContributionInfoMixin, CustomBaseModel):
    """A complete work of music

    A purely abstract entity that can manifest in differing versions.
    Divided into Sections.
    Must have at least one Section.
    In the case that a MusicalWork is not formally divided into Sections, it has
    one trivial Section that represents the whole work.

    Attributes
    ----------
    MusicalWork.variant_titles : ArrayField
        All the titles commonly attributed to this MusicalWork.

    MusicalWork.related_works : models.ManyToManyField
            MusicalWorks that are related to ths MusicalWork

    MusicalWork.genres_as_in_style : models.ManyToManyField
        References to GenreAsInStyle objects that are the style(s) of this
        MusicalWork

    MusicalWork.genres_as_in_type : models.ManyToManyField
        References to GenreAsInType objects that are the type(s) of this
        MusicalWork

    MusicalWork._sacred_or_secular : models.NullBooleanField
        Private property representing whether the MusicalWork is
        sacred, secular or none of those

    MusicalWork.authority_control_url : models.URLField
        An URL linking to an authority control description of this MusicalWork

    MusicalWork.authority_control_key : models.IntegerField
        The identifier of this MusicalWork in the authority control

    MusicalWork.contributions : models.ManyToOneRel
        References to Contributions objects that describe the contributions
        (and thus the contributors) of this MusicalWork

    MusicalWork.sections :  models.ManyToOneRel
        References to the Sections that are part of this MusicalWork

    MusicalWork.sources : models.ManyToOneRel
        References to Sources that instantiate this MusicalWork

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Section
    database.models.Part
    database.models.Contribution
    database.models.GenreAsInStyle
    database.models.GenreAsInType
    database.models.Source
    """

    variant_titles = ArrayField(
        models.CharField(max_length=200, blank=True),
        blank=False,
        null=False,
        default=list,
        help_text="All the titles commonly attributed to this "
        "musical work. Include the opus or catalogue number "
        "if there is one.",
    )
    related_works = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=True,
        help_text="MusicalWorks that are "
        "related to this "
        "MusicalWork, "
        "for instance, one is an "
        "arrangement of the other",
    )
    genres_as_in_style = models.ManyToManyField(
        "GenreAsInStyle",
        related_name="musical_works",
        help_text="e.g., classical, " "pop, folk",
    )
    genres_as_in_type = models.ManyToManyField(
        "GenreAsInType",
        related_name="musical_works",
        help_text="e.g., sonata, motet, " "12-bar blues",
    )
    _sacred_or_secular = models.NullBooleanField(
        null=True,
        blank=True,
        default=None,
        help_text="Leave blank if not " "applicable.",
    )
    authority_control_url = models.URLField(
        null=True,
        blank=True,
        help_text="URI linking to an "
        "authority control "
        "description of this "
        "musical work.",
    )
    authority_control_key = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        help_text="The identifier of "
        "this musical work "
        "in the authority "
        "control",
    )
    search_document = SearchVectorField(null=True, blank=True)

    class Meta(CustomBaseModel.Meta):
        db_table = "musical_work"
        verbose_name_plural = "Musical Works"
        indexes = [GinIndex(fields=["search_document"])]

    def __str__(self):
        return "{0}".format(self.variant_titles[0])

    @property
    def parts(self) -> QuerySet:
        """Get all the Parts related to this Musical Work."""
        part_model = apps.get_model("database", "part")
        parts = part_model.objects.none()
        for section in self.sections.all():
            parts.union(section.parts.all())
        return parts

    @property
    def instrumentation(self) -> QuerySet:
        """Get all the Instruments used in this Musical Work."""
        instrument_model = apps.get_model("database", "instrument")
        instruments = instrument_model.objects.none()
        for section in self.sections.all():
            instruments = instruments.union(section.instrumentation)
        return instruments

    @property
    def sacred_or_secular(self) -> str:
        """Get the sacred_or_secular value as a human friendly string."""
        if self._sacred_or_secular is None:
            return "Non Applicable"
        if self._sacred_or_secular:
            return "Sacred"
        if self._sacred_or_secular is False:
            return "Secular"
