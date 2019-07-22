"""Define a MusicalWork model"""
from django.apps import apps
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models import QuerySet
from database.mixins.file_and_source_mixin import FileAndSourceMixin
from database.models.custom_base_model import CustomBaseModel
from typing import List


class MusicalWork(FileAndSourceMixin, CustomBaseModel):
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
    sacred_or_secular = models.NullBooleanField(
        null=True, blank=True, default=None, help_text="Leave blank if not applicable."
    )
    contributors = models.ManyToManyField(
        "Person",
        through="ContributionMusicalWork",
        blank=True,
        help_text="The persons that contributed to the creation of this Musical Work",
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

    def __str__(self) -> str:
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
                )
            ),
            "D": (
                " ".join(
                    [entry.name for entry in self.arrangers]
                    + [entry.name for entry in self.performers]
                    + [entry.name for entry in self.transcribers]
                    + [entry.name for entry in self.improvisers]
                )
            ),
        }

    @property
    def section_parts(self) -> QuerySet:
        """Get all the Parts related to Sections of this Musical Work."""
        parts_model = apps.get_model("database", "part")
        parts = parts_model.objects.filter(id__in=self.sections.values_list("parts"))
        return parts

    @property
    def instrumentation(self) -> QuerySet:
        """Get all the Instruments used in this Musical Work."""
        instrument_model = apps.get_model("database", "instrument")
        ids = set()
        for section in self.sections.all():
            ids_list = list(section.instrumentation.values_list("id", flat=True))
            ids.update(ids_list)

        ids.update(list(self.parts.values_list("written_for", flat=True)))

        instruments = instrument_model.objects.filter(id__in=ids)
        return instruments

    @property
    def more_titles(self) -> List[str]:
        return self.variant_titles[1:]

    def _get_contributors_by_role(self, role: str) -> QuerySet:
        contributors = self.contributors.all().filter(
            contributions_works__role=role
        )
        return contributors

    @property
    def composers(self) -> QuerySet:
        """Get the Persons that are contributed as Composers.
        Returns
        -------
        composers : QuerySet
            A QuerySet of Person objects
        """
        return self._get_contributors_by_role("COMPOSER")

    @property
    def arrangers(self) -> QuerySet:
        """Get the Persons that are contributed as Arrangers.
        Returns
        -------
        arrangers : QuerySet
            A QuerySet of Person objects
        """
        return self._get_contributors_by_role("ARRANGER")

    @property
    def authors(self) -> QuerySet:
        """Get the Persons that are contributed as Authors of Text.
        Returns
        -------
        authors : QuerySet
            A QuerySet of Person objects
        """
        return self._get_contributors_by_role("AUTHOR")

    @property
    def transcribers(self) -> QuerySet:
        """Get the Persons that are contributed as Transcribers.
        Returns
        -------
        transcribers : QuerySet
            A QuerySet of Person objects
        """
        return self._get_contributors_by_role("TRANSCRIBER")

    @property
    def improvisers(self) -> QuerySet:
        """Get the Persons that are contributed as Improvisers.
        Returns
        -------
        improvisers : QuerySet
            A QuerySet of Person objects
        """
        return self._get_contributors_by_role("IMPROVISER")

    @property
    def performers(self) -> QuerySet:
        """Get the Persons that are contributed as Performers.
        Returns
        -------
        performers : QuerySet
            A QuerySet of Person objects
        """
        return self._get_contributors_by_role("PERFORMER")
