from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.musical_instance import MusicalInstance
from django.contrib.contenttypes.fields import GenericRelation
from database.models.instrument import Instrument


class Part(CustomBaseModel):
    title = models.CharField(max_length=200)
    instance = GenericRelation(MusicalInstance)
    written_for = models.ManyToManyField(Instrument,
                                         related_name='part_written_for')

    class Meta(CustomBaseModel.Meta):
        db_table = 'part'
