"""Define a Contribution model"""
from django.contrib.postgres.fields import DateRangeField
from django.core.exceptions import ValidationError
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class Contribution(CustomBaseModel):
    """ Relate a person that made a Contribution to a Musical Work/Section/Part

    A Contribution Model provides a many-to-many relationship with attributes
    between one of Musical Work, Section or Part to Person.

    A Musical Work/Section/Part can have many contributors with different roles
    i.e. a person composed a piece, two others arranged it, another wrote the
    lyrics.

    Contribution.person : models.ForeignKey
        Reference to a Person that made this Contribution to a Musical Work,
        Section or Part

    Contribution.certainty_of_attribution : models.BooleanField
        Whether it is certain if this Person made this Contribution

    ContributeTo.role : models.CharField
        The role that this Person had in contributing. Can be one of: Composer,
        Arranger, Author of Text, Transcriber, Improviser, Performer

    Contribution.date : postgres.fields.DateRangeField
        The date in which this Contribution happened

    Contribution.location : models.ForeignKey
        Reference to the GeographicArea in which this Contribution happened

    Contribution.contributed_to_part : models.ForeignKey
        Reference to the Part to which this Contribution was made

    Contribution.contributed_to_section : models.ForeignKey
        Reference to the Section to which this Contribution was made

    Contribution.contributed_to_work : models.ForeignKey
        Reference to the MusicalWork to which this Contribution was made

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Person
    database.models.MusicalWork
    database.models.Section
    database.models.Part
    database.models.GeographicArea
    """

    ROLES = (('COMPOSER', 'Composer'),
             ('ARRANGER', 'Arranger'),
             ('AUTHOR', 'Author of Text'),
             ('TRANSCRIBER', 'Transcriber'),
             ('IMPROVISER', 'Improviser'),
             ('PERFORMER', 'Performer'))
    person = models.ForeignKey('Person',
                               on_delete=models.PROTECT,
                               related_name='contributions',
                               help_text='The Person that contributed to a'
                                         'Musical Work, Section or Part')
    certain = models.BooleanField(default=True,
                                  null=False,
                                  blank=False,
                                  help_text='Whether it is '
                                            'certain if this '
                                            'Person made this '
                                            'contribution')
    role = models.CharField(default="COMPOSER",
                            max_length=30,
                            choices=ROLES,
                            help_text='The role that this Person had in '
                                      'contributing. Can be one of: Composer, '
                                      'Arranger, Author of Text, Transcriber, '
                                      'Improviser, Performer')
    date = DateRangeField(null=True,
                          blank=True,
                          help_text='The date in which this contribution '
                                    'happened')
    location = models.ForeignKey('GeographicArea',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 help_text='The location in which this '
                                           'contribution happened')
    contributed_to_part = models.ForeignKey('Part',
                                            null=True,
                                            blank=True,
                                            on_delete=models.CASCADE,
                                            related_name='contributions',
                                            help_text='The Part that the '
                                                      'Person contributed to')
    contributed_to_section = models.ForeignKey('Section',
                                               null=True,
                                               blank=True,
                                               on_delete=models.CASCADE,
                                               related_name='contributions',
                                               help_text='The Section that the '
                                                         'Person contributed '
                                                         'to')
    contributed_to_work = models.ForeignKey('MusicalWork',
                                            null=True,
                                            blank=True,
                                            on_delete=models.CASCADE,
                                            related_name='contributions',
                                            help_text='The Musical Work that '
                                                      'the Person contributed '
                                                      'to')

    class Meta(CustomBaseModel.Meta):
        db_table = 'contribution'
        verbose_name_plural = 'Contributions'
        # Adding the same constraints as the clean method but on the DB level
        db_constraints = {
            'at_least_one_is_not_null': 'check (contributed_to_section_id is '
                                        'not null or contributed_to_part_id '
                                        'is not null or '
                                        'contributed_to_work_id is not null)',
            'work_unique':              'check (NOT (contributed_to_work_id is '
                                        'not null '
                                        'and (contributed_to_section_id is not '
                                        'null or '
                                        'contributed_to_part_id is not null)))',
            'section_unique':           'check (NOT (contributed_to_section_id '
                                        'is not '
                                        'null '
                                        'and (contributed_to_work_id is not '
                                        'null or '
                                        'contributed_to_part_id is not null)))',
            'part_unique':              'check (NOT (contributed_to_part_id is '
                                        'not null '
                                        'and (contributed_to_section_id is not '
                                        'null or '
                                        'contributed_to_work_id is not null)))'
            }

    def __str__(self):
        if self.contributed_to_part_id is not None:
            return "{0}, {1} of {2}".format(self.person, self.role.lower(),
                                            self.contributed_to_part)
        if self.contributed_to_section_id is not None:
            return "{0}, {1} of {2}".format(self.person, self.role.lower(),
                                            self.contributed_to_section)
        if self.contributed_to_work_id is not None:
            return "{0}, {1} of {2}".format(self.person, self.role.lower(),
                                            self.contributed_to_work)

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
        if self.contributed_to_part_id is not None:
            if self.contributed_to_section_id is not None or \
                    self.contributed_to_work_id is not None:
                raise ValidationError('Only one of Work, Section or '
                                      'Part must be not null')
        if self.contributed_to_section_id is not None:
            if self.contributed_to_part_id is not None or \
                    self.contributed_to_work_id is not None:
                raise ValidationError('Only one of Work, Section or '
                                      'Part must be not null')
        if self.contributed_to_work_id is not None:
            if self.contributed_to_part_id is not None or \
                    self.contributed_to_section_id is not None:
                raise ValidationError('Only one of Work, Section or '
                                      'Part must be not null')
        if self.contributed_to_section_id is None and \
                self.contributed_to_part_id is None and \
                self.contributed_to_work_id is None:
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
