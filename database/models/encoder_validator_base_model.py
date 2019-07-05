"""Define a base model for Encoder and Validator"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, CheckConstraint

from database.models.custom_base_model import CustomBaseModel


class EncoderValidatorBaseModel(CustomBaseModel):
    """A abstract base model for Encoder and Validator.

    Attributes
    ----------
    EncoderValidatorBaseModel.work_flow_text : models.TextField
        A description of the workflow that was used to encode a File

    EncoderValidatorBaseModel.work_flow_file : models.FileField
        A file that describes or defines the workflow that was used to encode
        or validate a File in the database

    EncoderValidatorBaseModel.notes : models.TextField
        Any extra notes or remarks

    EncoderValidatorBaseModel.user : models.ForeignKey
        The User that encoded a File

    EncoderValidatorBaseModel.software : models.ForeignKey
        The User that encoded a File

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Encoder
    database.models.Validator
    database.models.User
    database.models.Software
    """

    work_flow_text = models.TextField(
        help_text="A description of the "
        "workflow that was used to "
        "encode or validate a File"
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
        "was used to encode or "
        "validate a File in the "
        "database",
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Any extra notes or remarks the User wishes to provide",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="The User that encoded or validated a File",
    )
    software = models.ForeignKey(
        "Software",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="The Software the encoded or validated a File",
    )

    class Meta(CustomBaseModel.Meta):
        abstract = True

    def clean(self) -> None:
        """Enforce the integrity of the relationship to Software or User

        Ensure that one and only one of Software or User is not null
        """
        if self.user_id is not None and self.software_id is not None:
            raise ValidationError("Both User and Software are set. One must be null")
        if self.user_id is None and self.software_id is None:
            raise ValidationError("Neither User and Software are set")
        super(CustomBaseModel, self).clean()
