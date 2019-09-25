"""Define an Archive model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class Archive(CustomBaseModel):
    """A location where Sources are stored.

    e.g: A database or a library.

    Attributes
    ----------
    Archive.name : models.CharField
        The name of the archive.

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Sources
    """

    name = models.CharField(
        max_length=200, blank=False, null=False, help_text="The name of the Archive"
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
