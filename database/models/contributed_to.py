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
    """Relates a person that contributed to a work/section/part

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
                               related_name='contributed_to')
    certain = models.BooleanField(default=True, null=False, blank=False)
    role = models.CharField(default="COMPOSER", max_length=30, choices=ROLES)
    date = DateRangeField(null=True, blank=True)
    location = models.ForeignKey(GeographicArea, on_delete=models.SET_NULL,
                                 null=True, blank=True)

    contributed_to_part = models.ForeignKey(Part, null=True,
                                            blank=True,
                                            on_delete=models.CASCADE,
                                            related_name='contributed_to')
    contributed_to_section = models.ForeignKey(Section, null=True,
                                               blank=True,
                                               on_delete=models.CASCADE,
                                               related_name='contributed_to')
    contributed_to_work = models.ForeignKey(MusicalWork, null=True,
                                            blank=True,
                                            on_delete=models.CASCADE,
                                            related_name='contributed_to')

    def __str__(self):
        if self.contributed_to_part_id is not None:
            return "{0}, {1} of {2}".format(self.person, self.role,
                                            self.contributed_to_part)
        if self.contributed_to_section_id is not None:
            return "{0}, {1} of {2}".format(self.person, self.role,
                                            self.contributed_to_section)
        if self.contributed_to_work_id is not None:
            return "{0}, {1} of {2}".format(self.person, self.role,
                                            self.contributed_to_work)
        raise AssertionError("Neither 'contributed_to_part', "
                             "'contributed_to_work' or "
                             "'contributed_to_section' are set")

    def clean(self):
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

    class Meta(CustomBaseModel.Meta):
        db_table = 'contributed_to'
        verbose_name_plural = 'Contributed To Relationships'
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
