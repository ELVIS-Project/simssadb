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
                                  related_name='manifested_by_Text_file',
                                  on_delete=models.CASCADE, null=False)
    file = models.FileField(upload_to='text_files/')

    languages = ArrayField(
            ArrayField(
                    models.CharField(max_length=200, blank=True)
            ),
            blank=True, null=True
    )

    def __str__(self):
        filename = os.path.basename(self.file.name)
        return "{0}".format(filename)

    class Meta(File.Meta):
        db_table = 'text_file'
