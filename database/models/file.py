from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.musical_instance import MusicalInstance


class File(CustomBaseModel):
    file_type = models.CharField(max_length=10)
    file_size = models.PositiveIntegerField()
    version = models.CharField(max_length=20, null=True)
    encoding_date = models.DateTimeField(null=True)
    manifests = models.ForeignKey(MusicalInstance, related_name='manifested_by',
                                  on_delete=models.CASCADE)

    class Meta:
        abstract = True
