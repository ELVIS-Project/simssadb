from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.instrument import Instrument
from database.models.section import Section


class Part(CustomBaseModel):
    """
    A single voice or instrument in a Section of a Musical Work

    Purely abstract entity that can manifest in differing versions.
    Must belong to one and only one Section
    """
    label = models.CharField(max_length=200)
    written_for = models.ManyToManyField(Instrument,
                                         related_name='part_written_for')
    in_section = models.ForeignKey(Section, on_delete=models.CASCADE,
                                   related_name='parts')
    contributors = models.ManyToManyField(
            'Person',
            through='ContributedTo',
            through_fields=(
                'contributed_to_part', 'person')
    )


    def __str__(self):
        return "{0}".format(self.label, )

    class Meta(CustomBaseModel.Meta):
        db_table = 'part'
