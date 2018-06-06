from django.db import models
from database.models.file import File
from database.models.musical_instance import MusicalInstance
from database.models.notation_type import NotationType
from database.models.instrument import Instrument


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
    manifests = models.ForeignKey(MusicalInstance,
                                  related_name='manifested_by_sym_file',
                                  on_delete=models.CASCADE)
    notated_in = models.ForeignKey(NotationType, on_delete=models.CASCADE)
    instruments_used = models.ManyToManyField(Instrument)


    class Meta:
        db_table = 'symbolic_music_file'
