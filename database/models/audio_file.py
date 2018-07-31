"""Define an AudioFile model"""
import os

from django.db import models

from database.models.file import File
from database.models.source import Source


class AudioFile(File):
    """A manifestation of a Source as an digital audio file

    Generated from a source by an Encoder and can be validate by a Validator

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
        The Source manifested by this AudioFile

    AudioFile.file : models.FileField
        The path to the actual file stored on disk

    See Also
    --------
    database.models.File : The super class of AudioFile
    database.models.CustomBaseModel
    database.models.Source

    """
    length = models.PositiveIntegerField(help_text='The length of this Audio '
                                                   'File in seconds')
    recording_date = models.DateField(help_text='The date this file was '
                                                'recorded', null=True,
                                      blank=True)
    manifests = models.ForeignKey(Source,
                                  related_name='manifested_by_audio_files',
                                  on_delete=models.CASCADE, null=False,
                                  help_text='The Source manifested by this '
                                            'Audio File')
    file = models.FileField(upload_to='audio/', help_text='The actual file')

    class Meta(File.Meta):
        db_table = 'audio_file'

    def __str__(self):
        filename = os.path.basename(self.file.name)
        return "{0}".format(filename)

    def _prepare_summary(self):
        """Prepare a dictionary that summarizes an instance of this model.

        Useful when listing many instances in a list-type view

        Returns
        -------
        summary : dict
            A dictionary containing the essential data to display this object
            in a list-type view

        See Also
        --------
        database.models.CustomBaseModel.summary: the property that validates
        the returned dictionary and exposes it to other classes

        """
        summary = {'display': self.__str__(),
                   'file_type': self.file_type,
                   'source': self.manifests.part_of_collection.title,
                   'url': self.get_absolute_url()
                   }
        return summary

    def detail(self):
        """Get all the data about this instance relevant to a user.

        Useful when displaying this object in a detail-type view

        Returns
        -------
        detail_dict : dict
            A dictionary containing the relevant data about this instance

        Warnings
        --------
        This method causes database calls and can be expensive, avoid using in a
        loop

        """
        detail_dict = {
            'title': self.__str__(),
            'length': self.length,
            'file_type': self.file_type,
            'version': self.version,
            'file_size': self.file_size,
            'recording_date': self.recording_date,
            'encoding_date': self.encoding_date,
            'encoded_with': self.encoded_with,
            'validated_by': self.validated_by,
            'extra_metadata': self.extra_metadata,
            'source': self.manifests,
            'file': self.file
            }

        return detail_dict
