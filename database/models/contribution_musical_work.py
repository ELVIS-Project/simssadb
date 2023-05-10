"""Defines a Contribution model"""
from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.contrib.postgres.fields import IntegerRangeField
from database.models.custom_base_model import CustomBaseModel
from psycopg2.extras import NumericRange
from database.utils.model_utils import range_to_str, clean_year_range
from typing import Optional
from django.core.exceptions import ValidationError


class ContributionMusicalWork(CustomBaseModel):
    """A Contribution made by a Person to a Musical Work

    A Contribution associates a Person with a Musical Work, defining a role for the
    Person (one of Composer, Arranger, Author of Text, Transcriber, Improviser or 
    Performer) along with associated data (certainty of attribution, date and location).

    A Person can contribute to a Musical Work in multiple roles, for instance as 
    Composer and Author of Text. However, those would be represented by two separate
    instances of the ContributionMusicalWork model.

    Attributes
    ----------
    certainty_of_attribution: models.NullBooleanField
        Whether it is certain if this Person made this Contribution.
        Can be certain (True), uncertain(False), or unknown(Null).

    contributed_to_work: models.ForeignKey
        A reference to the Musical Work associated with this Contribution

    date_range_year_only: IntegerRangeField
        An integer range representing an year range that this contribution was made.

        An integer range is used to allow for uncertain dates. The range thus represents
        a lower and upper bound on the years that this Contribution could possibly have
        occurred.

        Ranges in PostgreSQL are standardized to a ``[)`` interval, that is closed on 
        the lower bound and open on the upper bound. 

        If the date of the Contribution can be determined to one specific year, then 
        such year should be entered as the lower bound and the next year as the upper 
        bound (since the upper bound is open). For example, if the year is determined to 
        be 1750, the range should then be ``[1750, 1751)``.

        If the Contribution could have occurred between the years of 1749 and 1755, then
        the range should be ``[1749, 1756)`` to account for the open upper bound.

        Neither bound should be ``Null`` since PostgreSQL interprets those as infinity.

    location: models.ForeignKey
        A reference to the GeographicArea where this Contribution occurred.

    person: models.ForeignKey
        A reference to the Person responsible for this Contribution.

    role: models.CharField
        The role in which the Person made this Contribution. The possible roles are
        represented as tuples and defined in the ``ROLES`` constant
    """

    ROLES = (
        ("COMPOSER", "Composer"),
        ("ARRANGER", "Arranger"),
        ("AUTHOR", "Author of Text"),
        ("TRANSCRIBER", "Transcriber"),
        ("IMPROVISER", "Improviser"),
        ("PERFORMER", "Performer"),
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
    certainty_of_attribution = models.BooleanField(
        help_text="Whether it is certain if this Person made this contribution",
        null=True,
        blank=True,
    )
    date_range_year_only = IntegerRangeField(
        null=True,
        blank=True,
        help_text="The year range of this contribution. If the year is known precisely,"
        " enter only one value. If not, enter a lower and upper bound",
    )
    location = models.ForeignKey(
        "GeographicArea",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The location in which this contribution happened",
    )
    person = models.ForeignKey(
        "Person",
        related_name="contributions_works",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        help_text="The Person that contributed to a Musical Work",
    )
    contributed_to_work = models.ForeignKey(
        "MusicalWork",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="contributions",
        help_text="The Musical Work that the Person contributed to",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "contribution_musical_work"
        verbose_name_plural = "Contributions to Musical Works"
        verbose_name = "Contribution to Musical Work"
        constraints = [
            # Ensures that either the whole range is null or both bounds are not null
            # One of the bounds being null and not the other is not allowed, since
            # PostgreSQL treats a null bound as infinity.
            CheckConstraint(
                check=(
                    (
                        # Both bounds are not null
                        Q(date_range_year_only__startswith__isnull=False)
                        & Q(date_range_year_only__endswith__isnull=False)
                    )
                    # Or the whole range is null
                    | Q(date_range_year_only__isnull=True)
                ),
                name="contribution_date_range_bounds_not_null",
            )
        ]

    def __str__(self) -> str:
        return "{0}, {1} of {2}".format(
            self.person, self.role.lower(), self.contributed_to_work
        )

    def clean(self) -> None:
        """Validates the date ranges to conform to the proper bounds"""
        # Declare contributor_life_span and initialize it if it exists
        contributor_life_span: Optional[NumericRange] = None
        if (
            self.person.birth_date_range_year_only
            and self.person.death_date_range_year_only
        ):
            contributor_life_span = NumericRange(
                self.person.birth_date_range_year_only.lower,
                self.person.death_date_range_year_only.upper,
                bounds="[)",
            )
        # Check if the date range was defined. If yes, clean the range
        if self.date_range_year_only:
            temp_date_range = self.date_range_year_only
            self.date_range_year_only = clean_year_range(temp_date_range)
            # If date range was defined and the contributor has a life span,
            # check if date range is within the life span
            # This check would also be useful to write at the database level but since
            # it involves two tables, it cannot be done directly and would require the
            # use of database triggers
            if contributor_life_span:
                lower: int = self.date_range_year_only.lower
                upper: int = self.date_range_year_only.upper
                if (
                    lower < contributor_life_span.lower
                    or upper > contributor_life_span.upper
                ):
                    raise ValidationError(
                        "Date range is outside of contributor's life span"
                    )
        # If no range was defined, default to the life span of the contributor
        elif contributor_life_span:
            self.date_range_year_only = contributor_life_span

    @property
    def date(self) -> str:
        """Formats the date range into a front-end friendly display. 

        If the range is the same as the Person lifespan, returns an empty string.

        Returns
        -------
        str
            A front-end friendly representation of the date range as string. 
            An empty string if the date range is the same as the Person lifespan.
        """
        # Check if the date range is the same as the contributor's life span
        if (
            self.person.birth_date_range_year_only
            and self.person.death_date_range_year_only
        ):
            contributor_life_span = NumericRange(
                self.person.birth_date_range_year_only.lower,
                self.person.death_date_range_year_only.upper,
                bounds="[)",
            )
            contribution_date_range = self.date_range_year_only
            # If it is return empty string
            if contribution_date_range == contributor_life_span:
                return ""

        # If not return str version of the date range
        return range_to_str(self.date_range_year_only)
