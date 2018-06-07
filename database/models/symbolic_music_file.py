from django.db import models
from database.models.file import File
from database.models.musical_instance import MusicalInstance
from database.models.instrument import Instrument


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

    manifests = models.ForeignKey(MusicalInstance,
                                  related_name='manifested_by_sym_file',
                                  on_delete=models.CASCADE, null=False)


    class Meta:
        db_table = 'symbolic_music_file'
