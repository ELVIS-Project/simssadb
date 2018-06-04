from django.db import models
from database.models.file import File


class SymbolicMusicFile(File):
    accidentals_encoded = models.BooleanField()
    real_octave_used = models.BooleanField()
    tuning_system_specified = models.BooleanField()
    transposing_instrument = models.BooleanField()
    instrument_specified = models.BooleanField()
    tempo_specified = models.BooleanField()
    precise_rhythms_specified = models.BooleanField()
    steady_tempo = models.BooleanField()
    has_dynamic_markings = models.BooleanField()
    has_performance_markings = models.BooleanField()


    class Meta:
        db_table = 'symbolic_music_file'
