"""Define an ValidationWorkflow model"""
from django.db import models
from database.models.custom_base_model import CustomBaseModel


class ValidationWorkFlow(CustomBaseModel):
    persons = models.CharField(
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

    class Meta(CustomBaseModel.Meta):
        db_table = "validation_workflow"
        verbose_name_plural = "Validation Workflows"

    def __str__(self):
        validated_by = "Validated by: {0}".format(self.persons)
        if self.validator_sofware:
            validated_by += " with {0}".format(self.software.__str__())
        return validated_by
