"""Define a Contribution model"""
from django.db import models
from django.db.models import CheckConstraint, Q
from django.contrib.postgres.fields import IntegerRangeField
from database.models.custom_base_model import CustomBaseModel
from psycopg2.extras import NumericRange
from database.utils.model_utils import clean_range


class ContributionMusicalWork(CustomBaseModel):
    """A Contribution to a Musical Work
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
    certainty_of_attribution = models.NullBooleanField(
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
            CheckConstraint(
                check=(
                    (
                        Q(date_range_year_only__startswith__isnull=False)
                        & Q(date_range_year_only__endswith__isnull=False)
                    )
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
        if self.date_range_year_only:
            if (
                self.date_range_year_only.lower is None
                and self.date_range_year_only.upper is not None
            ):
                self.date_range_year_only = NumericRange(
                    self.date_range_year_only.upper,
                    self.date_range_year_only.upper + 1,
                    bounds="[)",
                )
            elif (
                self.date_range_year_only.lower is not None
                and self.date_range_year_only.upper is None
            ):
                self.date_range_year_only = NumericRange(
                    self.date_range_year_only.lower,
                    self.date_range_year_only.lower + 1,
                    bounds="[)",
                )
        elif (
            self.person.birth_date_range_year_only
            and self.person.death_date_range_year_only
        ):
            self.date_range_year_only = NumericRange(
                self.person.birth_date_range_year_only.lower,
                self.person.death_date_range_year_only.upper,
                bounds="[)",
            )

    @property
    def date(self) -> str:
        if self.person.birth_date_range_year_only and self.person.death_date_range_year_only:
            contributor_life_span = NumericRange(
                self.person.birth_date_range_year_only.lower,
                self.person.death_date_range_year_only.upper,
            )
            contribution_date_range = self.date_range_year_only
            if contribution_date_range == contributor_life_span:
                return ""
        return clean_range(self.date_range_year_only)
