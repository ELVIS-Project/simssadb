"""Define a MusicalWork model"""
from django.apps import apps
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models import QuerySet
from database.models.custom_base_model import CustomBaseModel


class MusicalWork(CustomBaseModel):
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
            MusicalWorks that are related to this MusicalWork

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

    MusicalWork.contributions : models.ManyToOneRel
        References to Contributions objects that describe the contributions
        (and thus the contributors) of this MusicalWork

    MusicalWork.sections :  models.ManyToOneRel
        References to the Sections that are part of this MusicalWork

    MusicalWork.source_instantiations : models.ManyToOneRel
        References to SourceInstantiations that instantiate this MusicalWork

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Section
    database.models.Part
    database.models.Contribution
    database.models.GenreAsInStyle
    database.models.GenreAsInType
    database.models.SourceInstantiation
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
        help_text="e.g., classical, opera, folk",
    )
    genres_as_in_type = models.ManyToManyField(
        "GenreAsInType",
        related_name="musical_works",
        help_text="e.g., sonata, motet, 12-bar blues",
    )
    _sacred_or_secular = models.NullBooleanField(
        null=True, blank=True, default=None, help_text="Leave blank if not applicable."
    )
    authority_control_url = models.URLField(
        null=True,
        blank=True,
        help_text="URI linking to an "
        "authority control "
        "description of this "
        "musical work.",
    )
    search_document = SearchVectorField(null=True, blank=True)

    class Meta(CustomBaseModel.Meta):
        db_table = "musical_work"
        verbose_name_plural = "Musical Works"
        indexes = [GinIndex(fields=["search_document"])]

    def __str__(self):
        return self.variant_titles[0]

    def index_components(self) -> dict:
        return {
            "A": (
                " ".join(self.variant_titles + [entry.name for entry in self.composers])
            ),
            "B": (
                " ".join(
                    list(self.genres_as_in_style.values_list("name", flat=True))
                    + list(self.genres_as_in_type.values_list("name", flat=True))
                    + list(self.collections_of_sources.values_list("title", flat=True))
                )
            ),
            "C": (
                " ".join(
                    list(self.sections.values_list("title", flat=True))
                    + list(self.instrumentation.values_list("name", flat=True))
                    + [entry.name for entry in self.composers_locations]
                )
            ),
            "D": (
                " ".join(
                    [entry.name for entry in self.arrangers]
                    + [entry.name for entry in self.arrangers_locations]
                    + [entry.name for entry in self.performers]
                    + [entry.name for entry in self.performers_locations]
                    + [entry.name for entry in self.transcribers]
                    + [entry.name for entry in self.transcribers_locations]
                    + [entry.name for entry in self.improvisers]
                    + [entry.name for entry in self.improvisers_locations]
                    + list(
                        self.symbolic_music_formats
                        if self.symbolic_music_formats
                        else []
                    )
                )
            ),
        }

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
        else:
            return "Secular"
