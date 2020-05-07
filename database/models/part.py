"""Defines a Part model"""
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, Q, QuerySet
from database.models.custom_base_model import CustomBaseModel
from django.apps import apps
from database.mixins.file_and_source_mixin import FileAndSourceMixin


class Part(FileAndSourceMixin, CustomBaseModel):
    """A single voice or instrument in a Section or Musical Work.

    Purely abstract entity that can manifest in differing versions.

    Attributes
    ----------
    name : models.CharField
        The name of this Part

    musical_work : models.ForeignKey
        A reference to the MusicalWork this Part directly belongs to (i.e. it does not 
        belong to a Section that belongs to a MusicalWork)

    section : models.ForeignKey
        A reference to the Section that this Part belongs to

    written_for : models.ForeignKey
        A reference to the Instrument for which this Part is written

    source_instantiations : models.fields.related_descriptors.ManyToManyDescriptor
        References to SourceInstantiations that instantiate this Part
    """

    name = models.CharField(
        max_length=200,
        help_text="The name of this Part (e.g. Guitar, Violin II)",
        blank=True,
        null=True,
    )
    written_for = models.ForeignKey(
        "Instrument",
        null=False,
        blank=False,
        related_name="parts",
        help_text="The Instrument or Voice for which this Part is written",
        on_delete=models.PROTECT,
    )
    musical_work = models.ForeignKey(
        "MusicalWork",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="parts",
        help_text="The MusicalWork to which this Part belongs",
    )
    section = models.ForeignKey(
        "Section",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="parts",
        help_text="The Section to which this Part belongs",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "part"
        verbose_name_plural = "Parts"
        constraints = [
            # Ensures that the Part belongs to either a MusicalWork and a Section,
            # not both
            CheckConstraint(
                check=(
                    (Q(section__isnull=True) & Q(musical_work__isnull=False))
                    | (Q(section__isnull=False) & Q(musical_work__isnull=True))
                ),
                name="work_xor_section",
            )
        ]

    def __str__(self):
        if self.name:
            name = str(self.name)
        else:
            name = str(self.written_for.name)
        if self.musical_work:
            return "{0} ({1})".format(name, self.musical_work.__str__())
        elif self.section:
            return "{0} ({1}, {2})".format(
                name, self.section.__str__(), self.section.musical_work.__str__()
            )
        else:
            return name

    def clean(self) -> None:
        """Ensure that only Part points to a Musical Work or a Section but not both

        Raises
        ------
        ValidationError
            Error if the Part points to both a Musical Work and a Section
        """
        if self.musical_work is not None and self.section is not None:
            raise ValidationError(
                "Part has to belong to either a MusicalWork or a Section, not both"
            )

    @property
    def composers(self) -> QuerySet:
        """Get the Persons that have contributed as Composers.
       
        Returns
        -------
        composers : QuerySet
            A QuerySet of Person objects
        """
        if self.musical_work:
            return self.musical_work.composers
        elif self.section:
            return self.section.musical_work.composers
