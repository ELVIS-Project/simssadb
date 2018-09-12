from django.core.exceptions import ValidationError
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class Source(CustomBaseModel):
    """
    Represents a document containing the music defining a Work/Section/Part

    Must be part of a Collection of Sources.
    """
    work = models.ForeignKey('MusicalWork',
                             null=True,
                             blank=True,
                             on_delete=models.PROTECT,
                             related_name='source_instantiations',
                             help_text='The Musical Work manifested in part '
                                       'or in full by this Source')
    sections = models.ManyToManyField('Section',
                                      blank=True,
                                      related_name='source_instantiations',
                                      help_text='The Section or Sections '
                                                'manifested in full by this '
                                                'Source')
    parts = models.ManyToManyField('Part',
                                   blank=True,
                                   related_name='source_instantiations',
                                   help_text='The Part or Parts '
                                             'manifested in full by this '
                                             'Source')

    class Meta(CustomBaseModel.Meta):
        db_table = 'source'

    def clean(self):
        """ Enforce the integrity of the relationship.

        Ensure that at least one and only one of Musical Work/Section/Part
        is not null.

        Raises
        ------
        ValidationError
            If more than one out Musical Work, Section or Part are not null
            or if all three are null
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

    def save(self, *args, **kwargs):
        """Save the current instance.

        Overrides the parent method to ensure that clean() is called before
        actually saving.

        """
        self.full_clean()
        super(CustomBaseModel, self).save()
