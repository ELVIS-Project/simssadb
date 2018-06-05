from django.db import models
from database.models.file import File
from database.models.musical_instance import MusicalInstance


class AudioFile(File):
    length = models.PositiveIntegerField()  # In seconds or milliseconds maybe?
    recording_date = models.DateField()
    manifests = models.ForeignKey(MusicalInstance, related_name='manifested_by_audio_file',
                                  on_delete=models.CASCADE)

    class Meta:
        db_table = 'audio_file'
