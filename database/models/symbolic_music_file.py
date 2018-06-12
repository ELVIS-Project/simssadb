from django.db import models
from database.models.file import File
from database.models.source import Source
from database.models.instrument import Instrument
import os


class SymbolicMusicFile(File):
    """Manifestation of a Musical Instance as a digital music file

    Generated from a Source by a Symbolic Encoder
    """
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
    instruments_used = models.ManyToManyField(Instrument)

    manifests = models.ForeignKey(Source,
                                  related_name='manifested_by_sym_file',
                                  on_delete=models.CASCADE, null=False)

    file = models.FileField(upload_to='symbolic_music/')

    def __str__(self):
        filename = os.path.basename(self.file.name)
        return "{0}".format(filename)


    class Meta:
        db_table = 'symbolic_music_file'
