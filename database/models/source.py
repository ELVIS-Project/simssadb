"""Define a Source model"""
from django.core.exceptions import ValidationError
from django.db import models

from database.models import CustomBaseModel


class Source(CustomBaseModel):
    """A document containing the music defining a MusicalWork or a
    set of Sections or a set of Parts.

    Must be part of a CollectionOfSources.
    If a CollectionOfSources contains only one Source, the Source is trivial
    but still must exist, i.e., an CollectionOfSources without at least one
    Source cannot exist.

    A Source can be derived from a parent Source, implying a chain of
    provenance.

    Attributes
    ----------
    Source.portion : models.CharField
        A description of which portion of the CollectionOfSources this Source
        represents, for instance, page numbers or folio

    Source.collection : models.ForeignKey
        Reference to the CollectionOfSources this Source belongs to

    Source.parent_source : models.ForeignKey
        Reference to the Source this Source was derived from

    Source.child_sources : models.ManyToOneRel
        References to Sources derived from this Source
    """
    collection = models.ForeignKey('CollectionOfSources',
                                   null=False,
                                   blank=False,
                                   on_delete=models.PROTECT,
                                   related_name='sources')

    portion = models.CharField(max_length=200,
                               null=False,
                               blank=False,
                               help_text=' A description of which portion of '
                                         'the CollectionOfSources this Source '
                                         'represents, for instance, '
                                         'page numbers or folio')
    parent_source = models.ForeignKey('self',
                                      null=True,
                                      blank=True,
                                      on_delete=models.PROTECT,
                                      related_name='child_sources')

    class Meta(CustomBaseModel.Meta):
        db_table = 'source'

    def __str__(self):
        if self.portion:
            return self.collection.__str__() + ' ' + self.portion
        else:
            return self.collection.__str__()
