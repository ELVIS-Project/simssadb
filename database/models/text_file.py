"""Define a TextFile model"""
import os

from django.contrib.postgres.fields import ArrayField
from django.db import models

from database.models.file import File


class TextFile(File):
    """A manifestation of a Source as an digital text file.

    Manifests one and only one Source.

    Generated by an Encoder and validated against a Source by a Validator.

    Attributes
    ----------
    TextFile.file_type : models.CharField
        The format of this TextFile

    TextFile.file_size : models.PositiveIntegerField
        The size of the this TextFile in bytes

    TextFile.version : models.CharField
        The version of the encoding schema of this TextFile

    TextFile.encoding_date : models.DateTimeField
        The date this TextFile was encoded

    TextFile.encoded_with : models.ForeignKey
        A reference to the Encoder of this TextFile

    TextFile.validated_by : models.ForeignKey
        A reference to the Validator of this TextFile

    TextFile.extra_metadata : django.contrib.postgres.fields.JSONField
        Any extra metadata associated with this TextFile

    TextFile.manifests : models.ForeignKey
        The Source manifested by this TextFile

    TextFile.file : models.FileField
        The path to the actual file stored on disk

    See Also
    --------
    database.models.File : The super class of TextFile
    database.models.CustomBaseModel
    database.models.Source
    database.models.Encoder
    database.models.Validator
    """
    manifests = models.ForeignKey('Source',
                                  related_name='manifested_by_text_files',
                                  on_delete=models.CASCADE,
                                  null=False,
                                  help_text='The Source '
                                            'manifested by this '
                                            'Text File')
    file = models.FileField(upload_to='text_files/',
                            help_text='The actual file')

    languages = ArrayField(models.CharField(max_length=200,
                                            blank=True),
                           blank=True,
                           null=True,
                           help_text='The languages used in this Text File')

    class Meta(File.Meta):
        db_table = 'text_file'

    def __str__(self):
        filename = os.path.basename(self.file.name)
        return "{0}".format(filename)
