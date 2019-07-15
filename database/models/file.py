"""Define a File model"""
from typing import List
import os
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import QuerySet

from database.models.custom_base_model import CustomBaseModel


class File(CustomBaseModel):
    """Base abstract model with fields common to all file types.

    Most if not all fields should be extracted automatically

    Attributes
    ----------
    File.file_type : models.CharField
        The type of this file (Symbolic Music, Image, Text or Audio)

    File.file_format : models.CharField
        The format of this File

    File.file_size : models.PositiveIntegerField
        The size of the this File in bytes

    File.version : models.CharField
        The version of the encoding schema of this File

    File.encoding_date : models.DateTimeField
        The date this File was encoded

    File.encoded_with : models.ForeignKey
        A reference to the Encoder of this File

    File.validated_by : models.ForeignKey
        A reference to the Validator of this File

    File.extra_metadata : django.contrib.postgres.fields.JSONField
        Any extra metadata associated with this File

    File.manifests : None
        Subclasses must override

    File.file : models.FileField
        The path to the actual file stored on disk
    """

    TYPES = (
        ("sym", "Symbolic Music"),
        ("txt", "Text"),
        ("img", "Image"),
        ("audio", "Audio"),
    )
    file_type = models.CharField(
        default="sym", max_length=10, choices=TYPES, help_text="The type of the file"
    )
    file_format = models.CharField(max_length=10, help_text="The format of the file")
    file_size = models.PositiveIntegerField(
        null=True, blank=True, help_text="The size of the file in bytes"
    )
    version = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="The version of the encoding schema i.e. MEI 2.0",
    )
    encoding_date = models.DateTimeField(
        null=True, help_text="The date the File was ncoded"
    )
    encoding_workflow = models.ForeignKey(
        "EncodingWorkflow",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The Encoding Worflow of this File",
    )
    validation_workflow = models.ForeignKey(
        "ValidationWorkflow",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The Validation Worflow of this File",
    )
    extra_metadata = JSONField(
        null=True, blank=True, help_text="Any extra metadata associated with the File"
    )
    instantiates = models.ForeignKey(
        "SourceInstantiation",
        related_name="files",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        help_text="The SourceInstantiation anifested by this File",
    )
    file = models.FileField(upload_to="user_files/", help_text="The actual file")

    class Meta(CustomBaseModel.Meta):
        db_table = "files"

    def __str__(self) -> str:
        return os.path.basename(self.file.name)

    @property

    @property
