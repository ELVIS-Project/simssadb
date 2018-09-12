"""Define a Section model"""
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet

from database.mixins.contribution_info_mixin import ContributionInfoMixin
from database.mixins.file_and_source_info_mixin import FileAndSourceInfoMixin
from database.models.custom_base_model import CustomBaseModel
from database.models.instrument import Instrument


class Section(FileAndSourceInfoMixin, ContributionInfoMixin, CustomBaseModel):
    """A component of a Musical Work e.g. an Aria in an Opera

    Can alternatively be a Musical Work in its entirety, in which case the
    Musical Work has a single trivial Section that represents the whole work.
    A purely abstract entity that can be manifested in differing versions.
    Divided into one or more Parts.
    A Section can be divided into more Sections.
    Must have at least one part.

    Attributes
    ----------
    Section.title : models.CharField
        The title of this section

    Section.musical_work : models.ForeignKey
        Reference to the MusicalWork of which this Section is part.
        A Section must reference a MusicalWork even if it has parent Sections.

    Section.ordering : models.PositiveIntegerField
        A number representing the position of this section within a MusicalWork

    Section.parent_sections : models.ManyToManyField
        Sections that contain this Section.

    Sections.child_sections : models.ManyToManyField
        Sections that are sub-Sections of this Section

    Sections.related_sections: models.ManyToManyField
        Sections that are related to this Section (i.e. derived from it, or
        the same music but used in a different MusicalWork)

    Sections.parts : models.ManyToOne
        The Parts that belong to this Section

    Section.sources : models.ManyToMany
        The Sources that manifest this Section

    Section.contributions : models.ManyToOne
        The Contributions of this Section

    See Also
    --------
    database.models.CustomBaseModel
    database.models.MusicalWork
    database.models.Part
    database.models.SourceInstantiation
    database.models.Contribution
    """
    title = models.CharField(max_length=200,
                             help_text='The title of this Section')
    musical_work = models.ForeignKey('MusicalWork', null=False, blank=False,
                                     on_delete=models.PROTECT,
                                     related_name='sections',
                                     help_text='Reference to the MusicalWork '
                                               'of which this Section is '
                                               'part. A Section '
                                               'must '
                                               'reference a MusicalWork even '
                                               'if it has parent Sections')
    ordering = models.PositiveIntegerField(null=True, blank=True,
                                           help_text='A number representing '
                                                     'the position of this '
                                                     'Section within a Musical '
                                                     'Work')
    parent_sections = models.ManyToManyField('self',
                                             related_name='child_sections',
                                             blank=True,
                                             help_text='Sections that contain '
                                                       'this Section',
                                             symmetrical=False)
    related_sections = models.ManyToManyField('self',
                                              blank=True,
                                              help_text='Sections that are '
                                                        'related to this '
                                                        'Section (i.e. '
                                                        'derived from it, '
                                                        'or the same music '
                                                        'but used in a '
                                                        'different '
                                                        'MusicalWork)',
                                              symmetrical=True)

    class Meta(CustomBaseModel.Meta):
        db_table = 'section'

    def __str__(self):
        return "{0}".format(self.title)

    def clean(self):
        """Ensure that only Sections with no children have parts

        Raises
        ------
        ValidationError
            If the Section being validated has child sections and also has Parts
        """
        if (self.is_node or self.is_root) and self.parts.exists():
            raise ValidationError('Only Sections with no children can have '
                                  'Parts')

    def save(self, *args, **kwargs):
        """Save the current instance.

        Overrides the parent method to ensure that clean() is called before
        actually saving.
        """
        self.full_clean()
        super(CustomBaseModel, self).save()

    @property
    def instrumentation(self) -> QuerySet:
        """Gets all the Instruments used in this Section"""
        instruments = Instrument.objects.none()
        for part in self.parts.all():
            instruments = instruments.union(Instrument.objects.filter(
                    pk=part.written_for.id))
        if not instruments and self.parent_sections.exists():
            for parent in self.parent_sections.all():
                instruments = instruments.union(parent.instrumentation)
        if not instruments and self.child_sections.exists():
            for child in self.child_sections.all():
                instruments = instruments.union(child.instrumentation)
        return instruments

    @property
    def is_leaf(self) -> bool:
        """Check if Section has no children but has parents"""
        if not self.child_sections.exists() and self.parent_sections.exists():
            return True
        else:
            return False

    @property
    def is_root(self) -> bool:
        """Check if Section has no parents but has children"""
        if not self.parent_sections.exists() and self.child_sections.exists():
            return True
        else:
            return False

    @property
    def is_node(self) -> bool:
        """Check if Section has both children and parents"""
        if self.parent_sections.exists() and self.child_sections.exists():
            return True
        else:
            return False

    @property
    def is_single(self) -> bool:
        """Check if Section has no children and no parents"""
        if not self.parent_sections.exists() and not \
                self.child_sections.exists():
            return True
        else:
            return False
