"""Define a Validator model"""
from database.models.encoder_validator_base_model import EncoderValidatorBaseModel
from django.db.models import CheckConstraint, Q


class Validator(EncoderValidatorBaseModel):
    """A User or Software that validated a file using a specific workflow.

    Attributes
    ----------
    Validator.work_flow_text : models.TextField
        A description of the workflow that was used to validate a File

    Validator.work_flow_file : models.FileField
        A file that describes or defines the workflow that was used to validate
        or validate a File in the database

    Validator.notes : models.TextField
        Any extra notes or remarks

    Validator.user : models.ForeignKey
        The User that validated a File

    Validator.software : models.ForeignKey
        The User that validated a File

    Validator.audiofile_set : models.ManyToOneRel
        References to AudioFiles that were validated by this Validator

    Validator.textfile_set : models.ManyToOneRel
        References to TextFiles that were validated by this Validator

    Validator.imagefile_set : models.ManyToOneRel
        References to ImageFiles that were validated by this Validator

    Validator.symbolicmusicfile_set : models.ManyToOneRel
        References to SymbolicMusicFiles that were validated by this Validator

    See Also
    --------
    database.models.CustomBaseModel
    database.models.EncoderValidatorBaseModel
    database.models.User
    database.models.Software
    database.models.AudioFile
    database.models.TextFile
    database.models.ImageFile
    database.models.SymbolicMusicFile
    """

    class Meta(EncoderValidatorBaseModel.Meta):
        db_table = "validator"
        constraints = [
            CheckConstraint(
                check=(
                    (Q(user__isnull=True) & Q(software__isnull=False))
                    | (Q(user__isnull=False) & Q(software__isnull=True))
                ),
                name="validator_user_xor_software"
            )
        ]

    def __str__(self):
        if self.user_id is not None:
            return "{0} as validator".format(self.user)
        if self.software_id is not None:
            return "{0} as validator".format(self.software)
        raise AssertionError("Neither User or Software is set")
