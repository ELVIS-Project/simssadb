"""Define a SourceInstantiation model"""
from django.core.exceptions import ValidationError
from django.db import models

from database.models import CustomBaseModel


class SourceInstantiation(CustomBaseModel):
    portion = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    source = models.ForeignKey(
        "Source",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="source_instantiations",
        help_text="The Source that this source Instantiation instantiates",
    )
    work = models.ForeignKey(
        "MusicalWork",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="source_instantiations",
        help_text="The Musical Work manifested in part "
        "or in full by this Source "
        "Instantiation",
    )
    sections = models.ManyToManyField(
        "Section",
        blank=True,
        related_name="source_instantiations",
        help_text="The Section or Sections "
        "manifested in full by this "
        "Source Instantiation",
    )
    parts = models.ManyToManyField(
        "Part",
        blank=True,
        related_name="source_instantiations",
        help_text="The Part or Parts "
        "manifested in full by this "
        "Source Instantiation",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "source_instantiation"
        verbose_name_plural = "Source Instantiations"

    def __str__(self):
        return "Instantiation of " + self.source.__str__()
