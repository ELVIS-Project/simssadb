from django.db import models
from database.models.file import File
from database.models.source import Source
from django.contrib.postgres.fields import ArrayField
import os


class TextFile(File):
    """
    A manifestation of a Source as a digital Text file

    Generated from a source by an encoder
    """
    manifests = models.ForeignKey(Source,
                                  related_name='manifested_by_text_files',
                                  on_delete=models.CASCADE, null=False,
                                  help_text='The Source manifested by this '
                                            'Text File')
    file = models.FileField(upload_to='text_files/',
                            help_text='The actual file')

    languages = ArrayField(
            ArrayField(
                    models.CharField(max_length=200, blank=True)
            ),
            blank=True, null=True,
            help_text='The languages used in this Text File'
    )

    def __str__(self):
        filename = os.path.basename(self.file.name)
        return "{0}".format(filename)

    def prepare_summary(self):
        summary = {'display':   self.__str__(),
                   'file_type': self.file_type,
                   'source':    self.manifests.part_of_collection.title,
                   'url':       self.get_absolute_url()
                   }
        return summary

    class Meta(File.Meta):
        db_table = 'text_file'
