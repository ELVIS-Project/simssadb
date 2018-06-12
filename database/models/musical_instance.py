from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.source import Source
from database.models.musical_work import MusicalWork
from database.models.section import Section
from database.models.part import Part


class MusicalInstance(CustomBaseModel):
    """An abstract entity defined by the music specified by a particular Source

    It corresponds to a particular instantiation of all or part of a Musical
    Work. It must have a Source, and it is manifested by files.
    The relationship to files is implemented using a GenericForeignKey
    """
    source = models.OneToOneField(Source, on_delete=models.CASCADE,
                                  related_name='source_of')
    work = models.ManyToManyField(MusicalWork)
    section = models.ManyToManyField(Section)
    part = models.ManyToManyField(Part)


    def __str__(self):
        return "Instance of {0}".format(self.source.title)

    class Meta(CustomBaseModel.Meta):
        db_table = 'musical_instance'
