from django.db import models
from database.models.file import File
from database.models.source import Source
from django.contrib.postgres.fields import ArrayField


class ImageFile(File):
    """
    A manifestation of a Source as digital images

    Generated from a source by an Encoder and can be validate by a Validator
    """
    manifests = models.ForeignKey(Source,
                                  related_name='manifested_by_image_files',
                                  on_delete=models.CASCADE, null=False,
                                  help_text='The Source manifested by these '
                                            'images')

    files = ArrayField(models.ImageField(upload_to='images/'),
                       null=False, blank=False,
                       help_text='The actual set of image files')

    @property
    def pages(self):
        """Gets the number of images, which is equal to the number of pages"""
        return self.files.__len__()

    def __str__(self):
        return "Images of {0}".format(self.manifests)

    class Meta:
        db_table = 'image_file'
