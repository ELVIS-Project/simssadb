"""Define a ContributedTo model"""
from django.contrib.postgres.fields import DateRangeField
from django.core.exceptions import ValidationError
from django.db import models

from database.mixins.helper_functions import clean_date
from database.models.custom_base_model import CustomBaseModel
from database.models.geographic_area import GeographicArea
from database.models.musical_work import MusicalWork
from database.models.part import Part
from database.models.person import Person
from database.models.section import Section


class ContributedTo(CustomBaseModel):
    """ Relate a person that made a Contribution to a Musical Work/Section/Part

    A ContributedToModel provides a many-to-many relationship with attributes
    between one of Musical Work, Section or Part to Person.

    A Musical Work/Section/Part can have many contributors with different roles
    i.e. a person composed a piece, two others arranged it, another wrote the
    lyrics

    ContributedTo.person : models.ForeignKey
        Reference to a Person that made this Contribution to a Musical Work,
        Section or Part

    ContributedTo.certainty_of_attribution : models.BooleanField
        Whether it is certain if this Person made this Contribution

    ContributeTo.role : models.CharField
        The role that this Person had in contributing. Can be one of: Composer,
        Arranger, Author of Text, Transcriber, Improviser, Performer

    ContributedTo.date : postgres.fields.DateRangeField
        The date in which this Contribution happened

    ContributedTo.location : models.ForeignKey
        Reference to the GeographicArea in which this Contribution happened

    ContributedTo.contributed_to_part : models.ForeignKey
        Reference to the Part to which this Contribution was made

    ContributedTo.contributed_to_section : models.ForeignKey
        Reference to the Section to which this Contribution was made

    ContributedTo.contributed_to_work : models.ForeignKey
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

    ROLES = (
        ('COMPOSER', 'Composer'),
        ('ARRANGER', 'Arranger'),
        ('AUTHOR', 'Author of Text'),
        ('TRANSCRIBER', 'Transcriber'),
        ('IMPROVISER', 'Improviser'),
        ('PERFORMER', 'Performer'),
        )
    person = models.ForeignKey(Person, on_delete=models.PROTECT,
                               related_name='contributed_to',
                               help_text='The Person that contributed to a'
                                         'Musical Work, Section or Part')
    certainty_of_attribution = models.BooleanField(default=True, null=False,
                                                   blank=False,
                                                   help_text='Whether it is '
                                                             'certain if this '
                                                             'Person made this '
                                                             'contribution')
    role = models.CharField(default="COMPOSER", max_length=30, choices=ROLES,
                            help_text='The role that this Person had in '
                                      'contributing. Can be one of: Composer, '
                                      'Arranger, Author of Text, Transcriber, '
                                      'Improviser, Performer')
    date = DateRangeField(null=True, blank=True,
                          help_text='The date in which this contribution '
                                    'happened')
    location = models.ForeignKey(GeographicArea, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 help_text='The location in which this '
                                           'contribution happened')

    contributed_to_part = models.ForeignKey(Part, null=True,
                                            blank=True,
                                            on_delete=models.CASCADE,
                                            related_name='contributed_to',
                                            help_text='The Part that the '
                                                      'Person contributed to')
    contributed_to_section = models.ForeignKey(Section, null=True,
                                               blank=True,
                                               on_delete=models.CASCADE,
                                               related_name='contributed_to',
                                               help_text='The Section that the '
                                                         'Person contributed to'
                                               )
    contributed_to_work = models.ForeignKey(MusicalWork, null=True,
                                            blank=True,
                                            on_delete=models.CASCADE,
                                            related_name='contributed_to',
                                            help_text='The Musical Work that '
                                                      'the Person contributed '
                                                      'to')

    class Meta(CustomBaseModel.Meta):
        db_table = 'contributed_to'
        verbose_name_plural = 'Contributed To Relationships'
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

    def _prepare_summary(self):
        """Prepare a dictionary that summarizes an instance of this model.

        Useful when listing many instances in a list-type view.

        Returns
        -------
        summary : dict
            A dictionary containing the essential data to display this object
            in a list-type view.

        See Also
        --------
        database.models.CustomBaseModel.summary: the property that validates
        the returned dictionary and exposes it to other classes.

        """
        summary = {
            'display':                  '',  # Empty because we don't want to
                                             # display anything in the
                                             # contribution card
            'url':                      self.person.get_absolute_url(),
            'role':                     self.role.lower(),
            'person':                   self.person.__str__(),
            'date':                     clean_date(self.date),
            'location':                 self.location,
            'certainty_of_attribution': self.certainty_of_attribution
            }

        return summary

    def detail(self):
        """Get all the data about this instance relevant to a user.

        Useful when displaying this object in a detail-type view.

        Returns
        -------
        detail_dict : dict
            A dictionary containing the relevant data about this instance.

        Warnings
        --------
        This method causes database calls and can be expensive, avoid using in a
        loop.

        """
        contrib_dict = dict(contributed_to_work=self.contributed_to_work,
                            contributed_to_section=self.contributed_to_section,
                            contributed_to_part=self.contributed_to_part)
        detail_dict = self.summary().update(contrib_dict)
        return detail_dict
