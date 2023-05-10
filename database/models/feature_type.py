"""Defines a FeatureType model"""
from django.db import models
from django.db.models import Max, Min
from database.models.custom_base_model import CustomBaseModel


class FeatureType(CustomBaseModel):
    """A category of Feature of which ExtractedFeatures are instances.

    Attributes
    ----------
    name: models.CharField
        The name of the FeatureType

    code: models.CharField
        The jSymbolic code of the FeatureType

    description: models.TextField
        A description of the FeatureType

    is_sequential: models.NullBooleanField
        Whether a feature can be extracted from sequential windows of a data
        instance (e.g. individual measures, sections, etc); a value of true
        means that it can, a value of false means that only one feature value
        may be extracted per instance (i.e. per symbolic feature file)

    dimensions: models.PositiveIntegerField
        The number of dimensions of the FeatureType

    min_val: models.FloatField
        The minimum value of this FeatureType across all files that have this
        feature

    max_val: models.FloatField
        The maximum value of this FeatureType across all files that have this
        feature

    instances: models.models.fields.related_descriptors.ReverseManyToOneDescriptor
        The ExtractedFeature objects that are instances of this FeatureType
    """

    name = models.CharField(
        max_length=200, blank=False, null=False, help_text="The name of the FeatureType"
    )
    code = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        help_text="The jSymbolic code of the FeatureType",
    )
    description = models.TextField(
        blank=True, help_text="A description of the FeatureType"
    )
    is_sequential = models.BooleanField(
        blank=True,
        null=True,
        help_text="whether a feature can "
        "be extracted from "
        "sequential windows of a "
        "data instance (e.g. "
        "individual measures, "
        "sections, etc.); a "
        "value of true means "
        "that it can, a value of "
        "false means that only "
        "one feature value may "
        "be extracted per "
        "instance (i.e. per "
        "symbolic feature file)",
    )
    dimensions = models.PositiveIntegerField(
        help_text="The number of dimensions of the FeatureType"
    )
    min_val = models.FloatField(
        null=True,
        blank=True,
        help_text="The minimum value of this "
        "FeatureType across all "
        "files that have this feature",
    )
    max_val = models.FloatField(
        null=True,
        blank=True,
        help_text="The maximum value of this "
        "FeatureType across all "
        "files that have this feature",
    )
    software = models.ForeignKey(
        "Software",
        null=False,
        blank=False,
        default="",
        related_name="feature_types",
        help_text="The software that extracts this feature type",
        on_delete=models.PROTECT,
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "feature"
        verbose_name_plural = "Features"

    def __str__(self):
        return self.name

    def max_and_min(self) -> None:
        """Update the max and min values of this FeatureType"""
        if self.dimensions == 1:
            self.max_val = self.instances.all().aggregate(max_val=Max("value"))[
                "max_val"
            ][0]
            self.min_val = self.instances.all().aggregate(min_val=Min("value"))[
                "min_val"
            ][0]
            self.save()

    @property
    def group(self) -> str:
        """Get the human readable group from the code of this FeatureType"""
        group = self.code.split("-")[0]
        if group == "C":
            return "Chords and Vertical Interval Features"
        elif group == "D":
            return "Dynamics Features"
        elif group == "I":
            return "Instrumentation Features"
        elif group == "T":
            return "Musical Texture Features"
        elif group == "M":
            return "Melodic Interval Features"
        elif group == "P":
            return "Pitch Statistics Features"
        elif group == "R":
            return "Rhythm Features"
        elif group == "RT":
            return "Rhythm and Tempo Features"
        else:
            return group
