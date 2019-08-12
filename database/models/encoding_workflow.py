"""Define an EncodingWorkflow model"""
from django.db import models
from database.models.custom_base_model import CustomBaseModel


class EncodingWorkFlow(CustomBaseModel):
    persons = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="The person(s) that validated a file",
    )
    work_flow_text = models.TextField(
        help_text="A description of the "
        "workflow that was used to "
        "encode a File"
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
        encoded_by = "Encoded by: {0}".format(self.persons)
        if self.encoding_sofware:
            encoded_by += " with {0}".format(self.software.__str__())
        return encoded_by
