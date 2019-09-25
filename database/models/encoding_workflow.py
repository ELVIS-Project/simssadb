"""Define an EncodingWorkflow model"""
from django.db import models
from database.models.custom_base_model import CustomBaseModel


class EncodingWorkFlow(CustomBaseModel):
    """A workflow used to encode a symbolic music file.

    The EncodingWorkFlow model stores information on how a symbolic music file was
    encoded to aid with reproducibility and provenance tracking.

    Attributes
    ----------
    encoder_names: models.CharField
        The names of the persons that encoded a file 
        This is simply a string and does **not** reference the Person model
    
    encoding_software: models.ForeignKey
        A reference to the Software used to encode a file
    
    file: models.ForeignKey
        A reference to the file that was encoded using this workflow
    
    notes: models.TextField
        Any extra notes or remarks the user wishes to provide
    
    workflow_file: models.FileField
        A configuration file that defines a software encoding workflow
    
    workflow_text: models.TextField
        A textual description of the workflow used to encode a file
    """
    encoder_names = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="The names of the persons that encoded a file",
    )
    workflow_text = models.TextField(
        help_text="A description of the "
        "workflow that was used to "
        "encode a File"
        "in the database",
        null=True,
        blank=True,
    )
    workflow_file = models.FileField(
        upload_to="workflows/",
        null=True,
        blank=True,
        help_text="A file that describes or "
        "defines the workflow that "
        "was used to encode a File in the "
        "database",
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Any extra notes or remarks the user wishes to provide",
    )
    encoding_sofware = models.ForeignKey(
        "Software",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="encoding_workflows",
        help_text="The Software that was used in this Encoding Workflow"
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "encoding_workflow"
        verbose_name_plural = "Encoding Workflows"

    def __str__(self):
        encoded_by = "Encoded by: {0}".format(self.names)
        if self.encoding_sofware:
            encoded_by += " with {0}".format(self.software.__str__())
        return encoded_by
