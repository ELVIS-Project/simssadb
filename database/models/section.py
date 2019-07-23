"""Define a Section model"""
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from database.models.custom_base_model import CustomBaseModel
from database.mixins.file_and_source_mixin import FileAndSourceMixin


class Section(FileAndSourceMixin, CustomBaseModel):
    """A component of a Musical Work e.g. an Aria in an Opera

    Can alternatively be a Musical Work in its entirety, in which case the
    Musical Work has a single trivial Section that represents the whole work.
    A purely abstract entity that can be manifested in differing versions.
    Divided into one or more Parts.
    A Section can be divided into more Sections.
    Must have at least one part.

    Attributes
    ----------
    Section.title : models.CharField
        The title of this section

    Section.musical_work : models.ForeignKey
        Reference to the MusicalWork of which this Section is part.
        A Section must reference a MusicalWork even if it has parent Sections.

    Section.ordering : models.PositiveIntegerField
        A number representing the position of this section within a MusicalWork

    Section.parent_sections : models.ManyToManyField
        Sections that contain this Section.

    Sections.child_sections : models.ManyToManyField
        Sections that are sub-Sections of this Section

    Sections.related_sections: models.ManyToManyField
        Sections that are related to this Section (i.e. derived from it, or
        the same music but used in a different MusicalWork)

    Sections.parts : models.ManyToOne
        The Parts that belong to this Section

    Section.sources : models.ManyToMany
        The Sources that manifest this Section

    Section.contributions : models.ManyToOne
        The Contributions of this Section

    See Also
    --------
    database.models.CustomBaseModel
    database.models.MusicalWork
    database.models.Part
    database.models.Source
    database.models.Contribution
    """

    title = models.CharField(max_length=200, help_text="The title of this Section")
    musical_work = models.ForeignKey(
        "MusicalWork",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="sections",
        help_text="Reference to the MusicalWork "
        "of which this Section is "
        "part. A Section "
        "must "
        "reference a MusicalWork even "
        "if it has parent Sections",
    )
    ordering = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="A number representing "
        "the position of this "
        "Section within a Musical "
        "Work",
    )
    parent_sections = models.ManyToManyField(
        "self",
        related_name="child_sections",
        blank=True,
        help_text="Sections that contain his Section",
        symmetrical=False,
    )
    related_sections = models.ManyToManyField(
        "self",
        blank=True,
        help_text="Sections that are "
        "related to this "
        "Section (i.e. "
        "derived from it, "
        "or the same music "
        "but used in a "
        "different "
        "MusicalWork)",
        symmetrical=True,
    )
    contributors = models.ManyToManyField(
        "Person",
        through="ContributionSection",
        blank=True,
        help_text="The persons that contributed to the creation of this Section",
    )
    type_of_section = models.ForeignKey(
        "TypeOfSection",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="sections",
        help_text="The type of this section, e.g. Aria, Minuet, Chorus, Bridge",
    )
    search_document = SearchVectorField(null=True, blank=True)

    class Meta(CustomBaseModel.Meta):
        db_table = "section"
        indexes = [GinIndex(fields=["search_document"])]

    def __str__(self):
        return "{0} ({1})".format(self.title, self.musical_work.__str__())

    def index_components(self) -> dict:
        return {
            "A": (" ".join([self.title] + [entry.name for entry in self.composers])),
            "B": (
                " ".join(
                    self.musical_work.variant_titles
                    + list(self.collections_of_sources.values_list("title", flat=True))
                )
            ),
            "C": (
                " ".join(
                    list(self.instrumentation.values_list("name", flat=True))
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
    def instrumentation(self) -> QuerySet:
        """Gets all the Instruments used in this Section"""
        instrument_model = apps.get_model("database", "instrument")
        ids = set()
        ids.add(self.parts.all().values_list("written_for", flat=True))
        instruments = instrument_model.objects.filter(id__in=ids)
        return instruments

    @property
    def is_leaf(self) -> bool:
        """Check if Section has no children but has parents"""
        if not self.child_sections.exists() and self.parent_sections.exists():
            return True
        else:
            return False

    @property
    def is_root(self) -> bool:
        """Check if Section has no parents but has children"""
        if not self.parent_sections.exists() and self.child_sections.exists():
            return True
        else:
            return False

    @property
    def is_node(self) -> bool:
        """Check if Section has both children and parents"""
        if self.parent_sections.exists() and self.child_sections.exists():
            return True
        else:
            return False

    @property
    def is_single(self) -> bool:
        """Check if Section has no children and no parents"""
        if not self.parent_sections.exists() and not self.child_sections.exists():
            return True
        else:
            return False
