from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.instrument import Instrument


class Part(CustomBaseModel):
    """A single voice or instrument in a Section of a Musical Work

    Purely abstract entity that can manifest in differing versions.
    Can exist in more than one Section and more than one Musical Work.
    """
    label = models.CharField(max_length=200)
    written_for = models.ManyToManyField(Instrument,
                                         related_name='part_written_for')


    def __str__(self):
        return "{0}".format(self.label, )

    class Meta(CustomBaseModel.Meta):
        db_table = 'part'
