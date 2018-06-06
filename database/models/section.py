from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.musical_instance import MusicalInstance
from django.contrib.contenttypes.fields import GenericRelation
from database.models.part import Part


class Section(CustomBaseModel):
    title = models.CharField(max_length=200)
    ordering = models.PositiveIntegerField()
    instance = GenericRelation(MusicalInstance)
    section_of = models.ManyToManyField('self', related_name='in_sections')
    has_part = models.ManyToManyField(Part, related_name='in_sections')

    class Meta(CustomBaseModel.Meta):
        db_table = 'section'
