from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.musical_instance import MusicalInstance
from django.contrib.contenttypes.fields import GenericRelation
from database.models.part import Part


class Section(CustomBaseModel):
    title = models.CharField(max_length=200)
    ordering = models.PositiveIntegerField()
    instance = GenericRelation(MusicalInstance)
    section_of = models.ForeignKey('self', on_delete=models.CASCADE)
    has_part = models.ForeignKey(Part, on_delete=models.SET_NULL)

    class Meta(CustomBaseModel.Meta):
        db_table = 'section'
