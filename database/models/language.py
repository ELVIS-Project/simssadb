"""Defines a Language model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class Language(CustomBaseModel):
    """Represents a Language (e.g. Latin, French, English)

    Attributes
    ----------
    name : models.CharField
        The name of this language

    Sources : models.models.fields.related_descriptors.ManyToManyDescriptor
        References to the Sources that have text written in this Language
    """

    name = models.CharField(
        max_length=200, blank=False, help_text="The name of the Language"
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.name
