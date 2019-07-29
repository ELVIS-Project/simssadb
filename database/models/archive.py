"""Define an Archive model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class Archive(CustomBaseModel):
    """A location where Collections of Sources are stored.

    e.g: A database or a library.

    Attributes
    ----------
    Archive.name : models.CharField
        The name of the archive.

    Archive.collections: models.ManyToManyField
        References to CollectionsOfSources contained by this Archive.

    See Also
    --------
    database.models.CustomBaseModel
    database.models.CollectionsOfSources
    """

    name = models.CharField(
        max_length=200, blank=False, null=False, help_text="The name of the Archive"
    )
    collections = models.ManyToManyField(
        "CollectionOfSources",
        related_name="in_archive",
        help_text="CollectionsOfSources that belong to this Archive",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "archive"

    def __str__(self):
        return self.name
