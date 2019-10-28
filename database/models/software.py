"""Defines a Software model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class Software(CustomBaseModel):
    """A Software that encoded, validated or extracted features from a file.

    Attributes
    ----------
    name : models.CharField
        The name of this Software

    version : models.CharField
        The version of this Software

    encoder_workflows: models.fields.related_descriptors.ReverseManyToOneDescriptor
        References to the instances that this Software was used as in a EncoderWorkflow

    validator_workflows : models.fields.related_descriptors.ReverseManyToOneDescriptor
        References to the instances that this Software was used in a ValidationWorkflow

    features : models.fields.related_descriptors.ReverseManyToOneDescriptor
        References to the ExtractedFeatures extracted with this Software

    feature_files : models.fields.related_descriptors.ReverseManyToOneDescriptor
        References to the FeatureFiles containing features extracted with this Software

    featuretypes : models.fields.related_descriptors.ReverseManyToOneDescriptor
        References to FeatureTypes that can be be extracted with this Software
    """

    name = models.CharField(
        blank=False, max_length=100, help_text="The name of the Software"
    )
    version = models.CharField(
        blank=True, default="", max_length=10, help_text="The version of the Software"
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "software"
        verbose_name_plural = "Software"

    def __str__(self):
        return "{0}".format(self.name)
