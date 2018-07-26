from django.db import models
from database.models.file import File
from database.models.source import Source
import os


class AudioFile(File):
    """
    A manifestation of a Musical Instance as an digital audio file

    Generated from a source by an Encoder and can be validate by a Validator
    """
    length = models.PositiveIntegerField(help_text='The length of the Audio '
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

    def __str__(self):
        filename = os.path.basename(self.file.name)
        return "{0}".format(filename)

    def prepare_summary(self):
        summary = {'display': self.__str__(),
                   'file_type': self.file_type,
                   'source': self.manifests.part_of_collection.title,
                   'url': self.get_absolute_url()
                   }
        return summary

    def detail(self):
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

    class Meta(File.Meta):
        db_table = 'audio_file'
