"""Define a Software model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class Software(CustomBaseModel):
    """A Software that encoded, validated or extracted features from a file.

    Attributes
    ----------
    Software.name : models.CharField
        The name of this Software

    Software.version : models.CharField
        The version of this Software

    Software.configuration_file : models.FileField
        A file that describes how the Software was configured when performing
        an encoding, validation or feature extraction task.

    Software.encoder_set : models.ManyToOneRel
        References to the instances that this Software was used as an Encoder

    Software.validator_set : models.ManyToOneRel
        References to the instances that this Software was used as a Validator

    Software.extractedfeature_set : models.ManyToOneRel
        References to the ExtractedFeatures extracted with this Software

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Encoder
    database.models.Validator
    """

    name = models.CharField(
        blank=False, max_length=100, help_text="The name of the Software"
    )
    version = models.CharField(
        blank=True, default="", max_length=10, help_text="The version of the Software"
    )
    configuration_file = models.FileField(
        blank=True,
        null=True,
        upload_to="workflows/",
        help_text="A file that describes "
        "how the Software was "
        "configured when "
        "performing an encoding, "
        "validation or extracting "
        "task",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "software"

    def __str__(self):
        return "{0}".format(self.name)
