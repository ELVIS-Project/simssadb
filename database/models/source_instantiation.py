"""Define a SourceInstantiation model"""
from django.core.exceptions import ValidationError
from django.db import models

from database.models import CustomBaseModel


class SourceInstantiation(CustomBaseModel):
    """An abstract entity defined by the music specified by a
    particular Source, which corresponds to a particular
    instantiation of all or part of a Musical Work, Sections or Parts.

    Manifested by Audio, Symbolic, Text or Image files.

    Attributes
    ----------
    SourceInstantiation.source : models.ForeignKey
        Reference to the Source instantiated by this SourceInstantiation

    SourceInstantiation.work : models.ForeignKey
        Reference to a MusicalWork defined in full by this SourceInstantiation

    SourceInstantiation.sections : models.ManyToManyField
        References to Sections defined in full by this SourceInstantiation

    SourceInstantiation.parts : models.ManyToManyField
        References to Parts defined in full by this SourceInstantiation

    SourceInstantiation.manifested_by_audio_files : models.ManyToOneRel
        References to AudioFiles that manifest this SourceInstantiation

    SourceInstantiation.manifested_by_text_files : models.ManyToOneRel
        References to TextFiles that manifest this SourceInstantiation

    SourceInstantiation.manifested_by_image_files : models.ManyToOneRel
        References to ImageFiles that manifest this SourceInstantiation

    SourceInstantiation.manifested_by_sym_files : models.ManyToOneRel
        References to SymbolicMusicFiles that manifest this SourceInstantiation

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Source
    database.models.SymbolicMusicFile
    database.models.TextFile
    database.models.ImageFile
    database.models.AudioFile
    database.models.MusicalWork
    database.models.Section
    database.models.Part
    """
    source = models.ForeignKey('Source',
                               null=False,
                               blank=False,
                               on_delete=models.PROTECT,
                               related_name='source_instantiations',
                               help_text='The Source that this '
                                         'SourceInstantiation instantiates')
    work = models.ForeignKey('MusicalWork',
                             null=True,
                             blank=True,
                             on_delete=models.PROTECT,
                             related_name='source_instantiation',
                             help_text='The Musical Work manifested in part '
                                       'or in full by this Source '
                                       'Instantiation')
    sections = models.ManyToManyField('Section',
                                      blank=True,
                                      related_name='source_instantiation',
                                      help_text='The Section or Sections '
                                                'manifested in full by this '
                                                'Source Instantiation')
    parts = models.ManyToManyField('Part',
                                   blank=True,
                                   related_name='source_instantiation',
                                   help_text='The Part or Parts '
                                             'manifested in full by this '
                                             'Source Instantiation')

    class Meta(CustomBaseModel.Meta):
        db_table = 'source_instantiation'

    def __str__(self):
        return 'Instantiation of ' + self.source.__str__()

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
