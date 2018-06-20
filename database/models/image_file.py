from django.db import models
from database.models.file import File
from database.models.source import Source
from django.contrib.postgres.fields import ArrayField


class ImageFile(File):
    """A manifestation of a Source as digital images"""
    manifests = models.ForeignKey(Source,
                                  related_name='manifested_by_image_file',
                                  on_delete=models.CASCADE, null=False)

    files = ArrayField(models.ImageField(upload_to='images/'),
                       null=False, blank=False)

    title = models.CharField(max_length=100, null=True, blank=True)

    @property
    def pages(self):
        return self.files.__len__()

    def __str__(self):
        return "Images of {0}".format(self.manifests)

    class Meta:
        db_table = 'image_file'
