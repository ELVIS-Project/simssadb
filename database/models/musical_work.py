from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import ArrayField
from database.models.genre import Genre
from database.models.section import Section
from database.models.part import Part


class MusicalWork(CustomBaseModel):
    title = models.CharField(max_length=200, blank=False)
    variant_titles = ArrayField(
            ArrayField(
                    models.CharField(max_length=200, blank=True)
            ),
            blank=True
    )
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    sections = models.ManyToManyField(Section)
    parts = models.ManyToManyField(Part)


    class Meta(CustomBaseModel.Meta):
        db_table = 'musical_work'
