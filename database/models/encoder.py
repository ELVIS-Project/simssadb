"""Define and Encoder model"""
from database.models.encoder_validator_base_model import EncoderValidatorBaseModel


class Encoder(EncoderValidatorBaseModel):
    """A User or Software that encoded a file using a specific workflow.

    Attributes
    ----------
    Encoder.work_flow_text : models.TextField
        A description of the workflow that was used to encode a File

    Encoder.work_flow_file : models.FileField
        A file that describes or defines the workflow that was used to encode
        or validate a File in the database

    Encoder.notes : models.TextField
        Any extra notes or remarks

    Encoder.user : models.ForeignKey
        The User that encoded a File

    Encoder.software : models.ForeignKey
        The User that encoded a File

    Encoder.audiofile_set : models.ManyToOneRel
        References to AudioFiles that were encoded by this Encoder
    
    Encoder.textfile_set : models.ManyToOneRel
        References to TextFiles that were encoded by this Encoder
    
    Encoder.imagefile_set : models.ManyToOneRel
        References to ImageFiles that were encoded by this Encoder
    
    Encoder.symbolicmusicfile_set : models.ManyToOneRel
        References to SymbolicMusicFiles that were encoded by this Encoder
    
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
        db_table = "encoder"

    def __str__(self):
        if self.user_id is not None:
            return "{0} (Encoder)".format(self.user)
        if self.software_id is not None:
            return "{0}".format(self.software)
