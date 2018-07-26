from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import DateRangeField
from django.core.exceptions import ValidationError
from database.models.person import Person
from database.models.geographic_area import GeographicArea
from database.models.musical_work import MusicalWork
from database.models.section import Section
from database.models.part import Part


class ContributedTo(CustomBaseModel):
    """
    Relates a person that contributed to a work/section/part

    A work/section/part can have many contributors with different roles
    i.e. a person composed a piece, two others arranged it, another wrote the
    lyrics
    A person can be related to a work, section or part.
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
    certain = models.BooleanField(default=True, null=False, blank=False,
                                  help_text='Whether it is certain if this '
                                            'Person made this contribution')
    role = models.CharField(default="COMPOSER", max_length=30, choices=ROLES,
                            help_text='The role that this Person had in '
                                      'contributing. Can be one of: Composer, '
                                      'Arranger, Author of Text, Transcriber, '
                                      'Improviser, Performer')
    date = DateRangeField(null=True, blank=True,
                          help_text='The date in which this contribution happened')
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
        raise AssertionError("Neither 'contributed_to_part', "
                             "'contributed_to_work' or "
                             "'contributed_to_section' are set")

    def clean(self):
        """ Enforces the integrity of the relationship to Work/Section/Part

        Ensures that at least one of the Work/Section/Part is not null.
        Ensures that only one of Work/Section/Part is not null.
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
        self.full_clean()
        super(CustomBaseModel, self).save()

    def detail(self):
        pass

    def __get_date(self):
        date = None
        if self.date is not None:
            if self.date.lower is not None and self.date.upper is not None:
                if self.date.lower.year == self.date.upper.year:
                    date = str(self.date.upper.year)
                else:
                    date = str(self.date.lower.year) + '-' + str(self.date.upper.year)
            if self.date.lower is not None and self.date.upper is None:
                date = str(self.date.lower.year)
            if self.date.lower is None and self.date.upper is not None:
                date = str(self.date.upper.year)
        return date

    def prepare_summary(self):
        date = self.__get_date()

        if self.location is not None:
            location = self.location.name
        else:
            location = None

        summary = {'display': '',
                   'url': self.person.get_absolute_url(),
                   'role': self.role.lower(),
                   'person': self.person.__str__(),
                   'date': date,
                   'location': location,
                   'certain': self.certain
                   }

        return summary

    def summary(self):
        return self.prepare_summary()

    class Meta(CustomBaseModel.Meta):
        db_table = 'contributed_to'
        verbose_name_plural = 'Contributed To Relationships'
        # Adding the same constraints as the clean method but on the DB level
        db_constraints = {
            'at_least_one_is_not_null': 'check (contributed_to_section_id is '
                                        'not null or contributed_to_part_id '
                                        'is not null or '
                                        'contributed_to_work_id is not null)',
            'work_unique': 'check (NOT (contributed_to_work_id is not null '
                           'and (contributed_to_section_id is not null or '
                           'contributed_to_part_id is not null)))',
            'section_unique': 'check (NOT (contributed_to_section_id is not '
                              'null '
                           'and (contributed_to_work_id is not null or '
                           'contributed_to_part_id is not null)))',
            'part_unique': 'check (NOT (contributed_to_part_id is not null '
                           'and (contributed_to_section_id is not null or '
                           'contributed_to_work_id is not null)))'
        }
