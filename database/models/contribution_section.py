"""Define a Contribution model"""
from django.core.exceptions import ValidationError
from django.db import models

from database.models.custom_base_model import CustomBaseModel
from database.models.contribution_base_model import ContributionBaseModel


class ContributionSection(ContributionBaseModel):
    """ Relate a person that made a Contribution to a Musical Work/Section/Part.

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

    Contribution.contributed_to_section : models.ForeignKey
        Reference to the Section to which this Contribution was made

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Person
    database.models.Section
    database.models.Part
    database.models.GeographicArea
    """

    person = models.ForeignKey(
        "Person",
        related_name="contributions_sections",
        on_delete=models.PROTECT,
        help_text="The Person that contributed to a Section",
    )
    contributed_to_section = models.ForeignKey(
        "Section",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="contributions",
        help_text="The Section that the Person contributed to",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "contribution_section"
        verbose_name_plural = "Contributions to Sections"
        verbose_name = "Contribution to Section"

    def __str__(self):
        return "{0}, {1} of {2}".format(
            self.person, self.role.lower(), self.contributed_to_section
        )
