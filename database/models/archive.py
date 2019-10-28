"""Defines an Archive model"""
from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Archive(CustomBaseModel):
    """An Archive (physical or digital) of Sources
    
    Attributes
    ----------
    name: models.CharField
        The name of the Archive

    url: models.URLField
        The URL of this Archive
    
    sources: models.ManyToManyField
        Many to many reference to Sources that belong to this Archive
    """

    name = models.CharField(
        max_length=200, blank=False, null=False, help_text="The name of this Archive"
    )
    url = models.URLField(blank=True, null=True, help_text="The URL of the Archive")
    sources = models.ManyToManyField(
        "Source",
        related_name="in_archive",
        help_text="Sources that belong to this Archive",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "archive"
        verbose_name_plural = "Archives"

    def __str__(self):
        return self.name
