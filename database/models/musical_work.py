from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import ArrayField
from database.models.genre import Genre
from database.models.section import Section
from database.models.part import Part
from django.contrib.contenttypes.fields import GenericRelation
from database.models.musical_instance import MusicalInstance


class MusicalWork(CustomBaseModel):
    title = models.CharField(max_length=200, blank=False)
    variant_titles = ArrayField(
            ArrayField(
                    models.CharField(max_length=200, blank=True)
            ),
            blank=True
    )
    genre_as_in_style = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True,
                                          related_name='style')
    genre_as_in_form = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True,
                                         related_name='form')
    sections = models.ManyToManyField(Section)
    parts = models.ManyToManyField(Part)
    instance = GenericRelation(MusicalInstance)


    class Meta(CustomBaseModel.Meta):
        db_table = 'musical_work'
