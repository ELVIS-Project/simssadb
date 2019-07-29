"""Define a Source model"""
from django.core.exceptions import ValidationError
from django.db import models
from django.apps import apps
from database.models import CustomBaseModel
from django.db.models import QuerySet


class Source(CustomBaseModel):
    """A document containing the music defining a MusicalWork or a
    set of Sections or a set of Parts.

    A Source can be derived from a parent Source, implying a chain of
    provenance.

    Attributes
    ----------
    Source.parent_source : models.ForeignKey
        Reference to the Source this Source was derived from

    Source.child_sources : models.ManyToOneRel
        References to Sources derived from this Source
    """
    portion = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    parent_source = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="child_sources",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "source"

    @property
    def files(self) -> QuerySet:
        file_model = apps.get_model("database", "file")
        return file_model.objects.filter(
            id__in=self.source_instantiations.values_list("files", flat=True)
        )
