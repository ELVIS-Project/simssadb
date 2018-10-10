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
    work = models.ForeignKey('MusicalWork',
                             null=True,
                             blank=True,
                             on_delete=models.PROTECT,
                             related_name='sources',
                             help_text='The Musical Work manifested in part '
                                       'or in full by this Source')
    sections = models.ManyToManyField('Section',
                                      blank=True,
                                      related_name='sources',
                                      help_text='The Section or Sections '
                                                'manifested in full by this '
                                                'Source')
    parts = models.ManyToManyField('Part',
                                   blank=True,
                                   related_name='sources',
                                   help_text='The Part or Parts '
                                             'manifested in full by this '
                                             'Source')

    class Meta(CustomBaseModel.Meta):
        db_table = 'source_instantiation'

    def __str__(self):
        return ""

    def clean(self) -> None:
        """ Enforce the integrity of the relationship.

        Ensure that at least one and only one of MusicalWork/Sections/Parts
        is not null.

        Raises
        ------
        ValidationError
            If more than one out MusicalWork, Sections or Parts are not null
            or if all three are null.
        """
        if self.work is not None:
            if self.sections.exists() or \
                    self.parts.exists():
                raise ValidationError('Only one of Work, Sections or '
                                      'Part must be not null')
        if self.sections.exists():
            if self.parts.exists() or \
                    self.work is not None:
                raise ValidationError('Only one of Work, Sections or '
                                      'Parts must be not null')
        if self.work is not None:
            if self.parts.exists() or \
                    self.sections.exists():
                raise ValidationError('Only one of Work, Sections or '
                                      'Parts must be not null')
        if not self.sections.exists() and \
                not self.parts.exists() and \
                self.work is None:
            raise ValidationError('At least one of Work, Section or Part '
                                  'must be not null')
        super(CustomBaseModel, self).clean()
