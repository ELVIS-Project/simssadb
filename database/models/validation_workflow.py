"""Define an ValidationWorkflow model"""
from django.db import models
from database.models.custom_base_model import CustomBaseModel


class ValidationWorkFlow(CustomBaseModel):
    """A workflow used to validate a symbolic music file.

    The ValidationWorkFlow model stores information on how a symbolic music file was
    validated to aid with reproducibility and provenance tracking.

    Attributes
    ----------
    validator_names: models.CharField
        The names of the persons that validated a file 
        This is simply a string and does **not** reference the Person model
    
    validator_software: models.ForeignKey
        A reference to the Software used to validate a file
    
    file: models.ForeignKey
        A reference to the file that was validated using this workflow
    
    notes: models.TextField
        Any extra notes or remarks the user wishes to provide
    
    workflow_file: models.FileField
        A configuration file that defines a software validation workflow
    
    workflow_text: models.TextField
        A textual description of the workflow used to validate a file
    """
    validator_names = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="The person(s) that validated a file",
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Any extra notes or remarks the user wishes to provide",
    )
    validator_sofware = models.ForeignKey(
        "Software",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="validation_workflows",
        help_text="The Software that was used in this Validation Workflow"
    )
    workflow_text = models.TextField(
        help_text="A description of the "
        "workflow that was used to "
        "validate a File"
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
        "was used to validate a File in the "
        "database",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "validation_workflow"
        verbose_name_plural = "Validation Workflows"

    def __str__(self):
        validated_by = "Validated by: {0}".format(self.persons)
        if self.validator_sofware:
            validated_by += " with {0}".format(self.software.__str__())
        return validated_by
