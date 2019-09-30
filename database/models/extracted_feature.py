"""Defines an ExtractedFeature model."""
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class ExtractedFeature(CustomBaseModel):
    """Content-based data extracted from a SymbolicMusicFile.

    Extracted with a Software.
    Must be a feature of one and only one SymbolicMusicFile.
    Must be a instance of a FeatureType.

    Attributes
    ----------
    instance_of_feature : models.ForeignKey
        A reference to the FeatureType of this ExtractedFeature

    value : ArrayField(models.FloatField)
        An array of the value(s) of this Extracted Feature. One dimensional features
        have only element in the array

    extracted_with : models.ForeignKey
        A reference to the Software that was used to extract this
        ExtractedFeature

    feature_of : models.ForeignKey
        A reference to to the SymbolicMusicFile from which this
        ExtractedFeature was extracted.

    feature_files: models.ManyToManyField
        Many to many references to Feature Files that contain this feature
    """

    instance_of_feature = models.ForeignKey(
        "FeatureType",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="instances",
    )
    value = ArrayField(
        models.FloatField(),
        help_text="The value of the Extracted Feature. Encoded "
        "as an array but if the Extracted Feature is "
        "scalar it is an array of length = 1",
    )
    extracted_with = models.ForeignKey(
        "Software",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        help_text="The Software used to extract this Extracted Feature",
    )
    feature_of = models.ForeignKey(
        "File",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="features",
        help_text="The File from which the feature was extracted",
    )
    feature_files = models.ManyToManyField(
        "FeatureFile",
        blank=False,
        related_name="features",
        help_text="The Feature Files that contain this feature",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "extracted_feature"
        verbose_name_plural = "Extracted Features"

    def __str__(self):
        if not self.is_histogram:
            return "{0}: {1}".format(self.instance_of_feature.name, self.value[0])
        else:
            return self.name

    def clean(self) -> None:
        """Check if length of value is the same as the declared dimensions"""
        if not (len(self.value) == self.instance_of_feature.dimensions):
            raise ValidationError(
                "The length of the value array must be the "
                "same as the dimension of the FeatureType"
            )
        super().clean()

    def save(self, *args, **kwargs) -> None:
        """Call the max_and_min() method of FeatureType after saving"""
        super().save(*args, **kwargs)
        self.instance_of_feature.max_and_min()

    @property
    def name(self) -> str:
        """Get the name of this ExtractedFeature"""
        return self.instance_of_feature.name

    @property
    def is_histogram(self) -> bool:
        """Check if this ExtractedFeature is a histogram

        ExtractedFeatures are histograms if their dimensions are more than 1.
        """
        if self.instance_of_feature.dimensions > 1 and len(self.value) > 1:
            return True
        else:
            return False

    @property
    def description(self) -> str:
        """Get the description of this ExtractedFeature"""
        return self.instance_of_feature.description

    @property
    def code(self) -> str:
        """Get the jSymbolic code of this ExtractedFeature"""
        return self.instance_of_feature.code

    @property
    def group(self) -> str:
        """Get the jSymbolic group of this ExtractedFeature"""
        return self.instance_of_feature.group
