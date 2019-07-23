"""Define an ValidationWorkflow model"""
from django.db import models
from database.models.custom_base_model import CustomBaseModel


class ValidationWorkFlow(CustomBaseModel):
    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        help_text="The name of the ValidationWorkflow",
    )
    work_flow_text = models.TextField(
        help_text="A description of the "
        "workflow that was used to "
        "validate a File"
        "in the database",
        null=True,
        blank=True,
    )
    work_flow_file = models.FileField(
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
    validator_sofware = models.ForeignKey(
        "Software",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="validation_workflows",
        help_text="The Software that was used in this Validation Workflow"
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "validation_workflow"

    def __str__(self):
        return self.name
