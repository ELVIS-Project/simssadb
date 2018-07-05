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

    class Meta(File.Meta):
        db_table = 'audio_file'
