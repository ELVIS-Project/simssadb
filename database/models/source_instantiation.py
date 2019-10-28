"""Define a SourceInstantiation model"""
from django.core.exceptions import ValidationError
from django.db import models

from database.models import CustomBaseModel


class SourceInstantiation(CustomBaseModel):
    """A instantiation of a musical source. 
    
    Relates a source to specific file(s) and to a musical work, sections or parts.

    Attributes
    ----------
    portion : models.CharField
        The portion of the source represented by a file, to be used if the file does not
        represent the whole of the source (for example if the file represents only one
        movement but the source itself is the whole symphony)

    source : models.ForeignKey
        A reference to the source represented by the file linked to this source instantiation

    work : models.ForeignKey
        The Musical Work manifested in part or in full by this Source Instantiation

    sections : models.ManyToManyField
        The Section(s) manifested in full by this Source Instantiation

    parts : models.ManyToManyField
        The Part(s) manifested in full by this Source Instantiation

    files : models.fields.related_descriptors.ReverseManyToOneDescriptor
        The files that instantiate the Source linked to this SourceInstantiation
    """
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
        help_text="The source represented by the file linked to this source instantiation",
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
