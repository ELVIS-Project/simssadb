"""Define a Contribution model"""
from django.contrib.postgres.fields import DateRangeField
from django.core.exceptions import ValidationError
from django.db import models

from database.models.custom_base_model import CustomBaseModel
from database.utils.model_utils import clean_date


class ContributionBaseModel(CustomBaseModel):
    """An abstract model to define a Contribution to a Musical Work or Section.

    The Contribution Model provides a many-to-many relationship with attributes
    between one of Musical Work, Section or Part and Person.

    Each Contribution relates a Person to exclusively one of MusicalWork,
    Section or Part.

    A Musical Work/Section/Part can have many Contributions, since each of
    piece of music can have many contributors with different roles
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

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Person
    database.models.GeographicArea
    """

    ROLES = (
        ("COMPOSER", "Composer"),
        ("ARRANGER", "Arranger"),
        ("AUTHOR", "Author of Text"),
        ("TRANSCRIBER", "Transcriber"),
        ("IMPROVISER", "Improviser"),
        ("PERFORMER", "Performer"),
    )
    person = models.ForeignKey(
        "Person",
        on_delete=models.PROTECT,
        help_text="The Person that contributed to a Musical Work, Section or Part",
    )
    certainty_of_attribution = models.NullBooleanField(
        help_text="Whether it is certain if this Person made this contribution"
    )
    role = models.CharField(
        default="COMPOSER",
        max_length=30,
        choices=ROLES,
        help_text="The role that this Person had in "
        "contributing. Can be one of: Composer, "
        "Arranger, Author of Text, Transcriber, "
        "Improviser, Performer",
    )
    _date = DateRangeField(
        null=True, blank=True, help_text="The date in which this contribution happened"
    )
    location = models.ForeignKey(
        "GeographicArea",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The location in which this contribution happened",
    )

    class Meta(CustomBaseModel.Meta):
        abstract = True

    @property
    def date(self) -> str:
        return clean_date(self._date)
