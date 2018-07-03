from django.db import models

from database.mixins.file_and_source_info import FileAndSourceInfoMixin
from database.models.custom_base_model import CustomBaseModel
from database.models.instrument import Instrument
from database.models.section import Section


class Part(FileAndSourceInfoMixin, CustomBaseModel):
    """
    A single voice or instrument in a Section of a Musical Work

    Purely abstract entity that can manifest in differing versions.
    Must belong to one and only one Section
    """
    label = models.CharField(max_length=200,
                             help_text='Any label that could help describe '
                                       'this Part')
    written_for = models.ForeignKey(Instrument,
                                    related_name='part_written_for',
                                    help_text='The Instrument or Voice '
                                              'for which this Part is '
                                              'written',
                                    on_delete=models.PROTECT)

    in_section = models.ForeignKey(Section, on_delete=models.CASCADE,
                                   related_name='parts', default="",
                                   help_text='The Section to which this Part '
                                             'belongs')
    contributors = models.ManyToManyField(
            'Person',
            through='ContributedTo',
            through_fields=(
                'contributed_to_part', 'person'),
            help_text='All the People that '
                      'contributed to this '
                      'Part in different '
                      'capacities such as '
                      'composer or arranger'
            )


    def __str__(self):
        return "{0}".format(self.label, )

    class Meta(CustomBaseModel.Meta):
        db_table = 'part'
