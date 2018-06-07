from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.musical_instance import MusicalInstance
from django.contrib.contenttypes.fields import GenericRelation
from database.models.instrument import Instrument
from database.models.contributed_to import ContributedTo


class Part(CustomBaseModel):
    """A single voice or instrument in a Section of a Musical Work

    Purely abstract entity that can manifest in differing versions.
    Can exist in more than one Section and more than one Musical Work.
    """
    title = models.CharField(max_length=200)
    instance = GenericRelation(MusicalInstance)
    written_for = models.ManyToManyField(Instrument,
                                         related_name='part_written_for')
    contributor_relations = GenericRelation(ContributedTo)

    class Meta(CustomBaseModel.Meta):
        db_table = 'part'
