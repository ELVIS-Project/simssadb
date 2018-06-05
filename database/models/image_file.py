from django.db import models
from database.models.file import File
from database.models.musical_instance import MusicalInstance


class ImageFile(File):
    color_mode = models.CharField(max_length=20)
    compression_type = models.CharField(max_length=20)
    gama_correction = models.CharField(max_length=20)
    color_calibration = models.CharField(max_length=20)
    pixel_width = models.PositiveIntegerField()
    pixel_height = models.PositiveIntegerField()
    ppi = models.PositiveIntegerField()
    manifests = models.ForeignKey(MusicalInstance, related_name='manifested_by_image_file',
                                  on_delete=models.CASCADE)

    class Meta:
        db_table = 'image_file'
