"""Define an AudioFile model"""
import os

from django.db import models

from database.models.file import File


class AudioFile(File):
    """A manifestation of a Source as an digital audio file.

    Manifests one and only one Source.

    Generated by an Encoder and validated against a SourceInstantiation by a
    Validator.

    Attributes
    ----------
    AudioFile.file_type : models.CharField
        The format of this AudioFile

    AudioFile.file_size : models.PositiveIntegerField
        The size of the this AudioFile in bytes

    AudioFile.version : models.CharField
        The version of the encoding schema of this AudioFile

    AudioFile.encoding_date : models.DateTimeField
        The date this AudioFile was encoded

    AudioFile.encoded_with : models.ForeignKey
        A reference to the Encoder of this AudioFile

    AudioFile.validated_by : models.ForeignKey
        A reference to the Validator of this AudioFile

    AudioFile.extra_metadata : django.contrib.postgres.fields.JSONField
        Any extra metadata associated with this AudioFile

    AudioFile.length : models.PositiveIntegerField
        The length of this AudioFile in seconds

    AudioFile.recording_date : models.DateField
        The date this AudioFile was recorded

    AudioFile.manifests : ForeignKey
        The SourceInstantiation manifested by this AudioFile

    AudioFile.file : models.FileField
        The path to the actual file stored on disk

    See Also
    --------
    database.models.File : The super class of AudioFile
    database.models.CustomBaseModel
    database.models.Source
    database.models.Encoder
    database.models.Validator
    """
    length = models.PositiveIntegerField(help_text='The length of this Audio '
                                                   'File in seconds')
    recording_date = models.DateField(help_text='The date this file was '
                                                'recorded',
                                      null=True,
                                      blank=True)
    manifests = models.ForeignKey('SourceInstantiation',
                                  related_name='manifested_by_audio_files',
                                  on_delete=models.CASCADE,
                                  null=False,
                                  help_text='The SourceInstantiation '
                                            'manifested by this '
                                            'Audio File')
    file = models.FileField(upload_to='audio/',
                            help_text='The actual file')

    class Meta(File.Meta):
        db_table = 'audio_file'

    def __str__(self):
        filename = os.path.basename(self.file.name)
        return "{0}".format(filename)
