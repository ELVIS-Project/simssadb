"""Defines a FeatureFile model"""
from database.models import CustomBaseModel
from django.db import models


class FeatureFile(CustomBaseModel):
    """A file containing all the features extracted from a symbolic music file
    
    Attributes
    ----------
    file_format: models.CharField
        The format of this FeatureFile

    file: models.FileField
        The actual file with the features

    config_file: models.FileField
        A file specifying the configuration used to extract the features
        Used for reproducibility purposes

    feature_definition_file: models.FileField
        A file that defines the features represented in the feature file

    features_from_file: models.ForeignKey
        A reference to a File model from which these features were extracted

    extracted_with: models.ForeignKey
        A reference to the Software used to extract these features
    """

    file_format = models.CharField(
        max_length=255, help_text="The format of the FeatureFile"
    )
    file = models.FileField(
        upload_to="user_files/feature_files",
        max_length=500,
        help_text="The actual feature file"
    )
    config_file = models.FileField(
        upload_to="user_files/extracted_features",
        max_length=255,
        help_text="A file describing the configuration used to extract the features",
    )
    feature_definition_file = models.FileField(
        upload_to="user_files/extracted_features",
        max_length=255,
        help_text="A file that defines the features represented in the FeatureFile",
    )
    features_from_file = models.ForeignKey(
        "File",
        related_name="feature_files",
        null=False,
        help_text="The File that the features were extracted from",
        on_delete=models.CASCADE,
    )
    extracted_with = models.ForeignKey(
        "Software",
        on_delete=models.PROTECT,
        related_name="feature_files",
        null=False,
        blank=False,
        help_text="The Software used to extract these features",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "feature_file"
        verbose_name_plural = "Feature Files"
