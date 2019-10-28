"""Define a TypeOfSection model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class TypeOfSection(CustomBaseModel):
    """Represents a type of section (e.g. Aria, Allegro, Chorus, Bridge)

    Attributes
    ----------
    name : models.CharField
        The name of this type of section

    sections : models.models.fields.related_descriptors.ManyToManyDescriptor
        References to the Sections of this type
    """

    name = models.CharField(
        max_length=200, blank=False, help_text="The name of this Type of Section"
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "type_of_section"
        verbose_name_plural = "Types of Section"

    def __str__(self):
        return self.name
