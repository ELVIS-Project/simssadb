"""Defines a Section model"""
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from database.models.custom_base_model import CustomBaseModel
from database.mixins.file_and_source_mixin import FileAndSourceMixin


class Section(FileAndSourceMixin, CustomBaseModel):
    """A section of a Musical Work e.g. an Aria in an Opera
    
    A purely abstract entity that can be manifested in differing versions.
    A Section can be divided into one or more sub-Sections.
    Can contain one or more Parts.

    Attributes
    ----------
    title : models.CharField
        The title of this section

    musical_work : models.ForeignKey
        Reference to the MusicalWork of which this Section is part.
        A Section must reference a MusicalWork even if it has parent Sections.

    ordering : models.PositiveIntegerField
        A number representing the position of this section within a MusicalWork

    parent_section : models.ForeignKey
        A Section that contain this Section

    child_sections : models.fields.related_descriptors.ReverseManyToOneDescriptor
        Sections that are sub-Sections of this Section

    related_sections: models.ManyToManyField
        Sections that are related to this Section (i.e. derived from it, or
        the same music but used in a different MusicalWork)

    parts : models.fields.related_descriptors.ReverseManyToOneDescriptor
        The Parts that belong to this Section

    source_instantiations : models.fields.related_descriptors.ManyToManyDescriptor
        References to SourceInstantiations that instantiate this Section

    type_of_section : models.ForeignKey
        Reference to a TypeOfSection object
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
    parent_section = models.ForeignKey(
        "self",
        related_name="child_sections",
        null=True,
        blank=True,
        help_text="Sections that contain his Section",
        on_delete=models.PROTECT,
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
    type_of_section = models.ForeignKey(
        "TypeOfSection",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="sections",
        help_text="The type of this section, e.g. Aria, Minuet, Chorus, Bridge",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "section"
        verbose_name_plural = "Sections"

    def __str__(self):
        return "{0}".format(self.title)

    @property
    def instrumentation(self) -> QuerySet:
        """Gets all the Instruments used in this Section
        
        Returns
        -------
        QuerySet
            A QuerySet of Instrument objects
        """
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

    @property
    def composers(self) -> QuerySet:
        """Get the Persons that have contributed as Composers.
       
        Returns
        -------
        composers : QuerySet
            A QuerySet of Person objects
        """
        return self.musical_work.composers
