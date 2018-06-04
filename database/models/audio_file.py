from django.db import models
from database.models.file import File


class AudioFile(File):
    length = models.PositiveIntegerField()  # In seconds or milliseconds maybe?
    recording_date = models.DateField()


    class Meta:
        db_table = 'audio_file'
