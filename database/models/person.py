"""Define a Person model"""
from django.apps import apps
from django.contrib.postgres.fields import IntegerRangeField
from django.db import models
from django.db.models import QuerySet, CheckConstraint, Q
from psycopg2.extras import NumericRange
from database.utils.model_utils import clean_range
from database.models.custom_base_model import CustomBaseModel


class Person(CustomBaseModel):
    """A real world person that contributed to a MusicalWork/Section/Part

    Attributes
    ----------
    Person.given_name : models.CharField
        The given name of this Person

    Person.surname : models.CharField
        The surname of this Person

    Person.range_date_birth : django.contrib.postgres.fields.DateRangeField
        The possible range of dates of the birth of this Person
        If the date is know, then the beginning and end of range will be equal

    Person.range_date_death : django.contrib.postgres.fields.DateRangeField
        The possible range of dates of the death of this Person
        If the date is know, then the beginning and end of range will be equal

    Person.birth_location : models.ForeignKey
        Reference to the GeographicArea where this Person was born

    Person.death_location : models.ForeignKey
        Reference to the GeographicArea where this Person died

    Person.authority_control_url : models.URLField
        An URL linking to an authority control description of this Person

    Person.contributions : models.ManyToOneRel
        References to the Contributions made by this Person

    See Also
    --------
    database.models.CustomBaseModel
    database.models.GeographicArea
    database.models.Contribution
    """

    given_name = models.CharField(
        max_length=100,
        blank=False,
        help_text="The given name of this Person",
        default="",
    )
    surname = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="The surname of this Person, eave blank if it is unknown",
    )
    birth_date_range_year_only = IntegerRangeField(
        null=True,
        blank=True,
        help_text="The birth year range of this person. If the year is known precisely,"
        " enter only one value. If not, enter a lower and upper bound",
    )
    death_date_range_year_only = IntegerRangeField(
        null=True,
        blank=True,
        help_text="The death year range of this person. If the year is known precisely,"
        " enter only one value. If not, enter a lower and upper bound",
    )
    birth_location = models.ForeignKey(
        "GeographicArea",
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="birth_location_of",
        help_text="The birth location of this "
        "Person. Choose the most "
        "specific possible.",
    )
    death_location = models.ForeignKey(
        "GeographicArea",
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="death_location_of",
        help_text="The death location of this "
        "Person. Choose the most "
        "specific possible.",
    )
    authority_control_url = models.URLField(
        blank=True,
        null=True,
        help_text="An URI linking to an "
        "authority control "
        "description of this "
        "Person",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "person"
        verbose_name_plural = "Persons"
        constraints = [
            CheckConstraint(
                check=(
                    (
                        Q(birth_date_range_year_only__startswith__isnull=False)
                        & Q(birth_date_range_year_only__endswith__isnull=False)
                    )
                    | Q(birth_date_range_year_only__isnull=True)
                ),
                name="person_birth_range_bounds_not_null",
            ),
            CheckConstraint(
                check=(
                    (
                        Q(death_date_range_year_only__startswith__isnull=False)
                        & Q(death_date_range_year_only__endswith__isnull=False)
                    )
                    | Q(death_date_range_year_only__isnull=True)
                ),
                name="person_death_range_bounds_not_null",
            )
        ]


    def clean(self) -> None:
        if self.birth_date_range_year_only:
            if (
                self.birth_date_range_year_only.lower is None
                and self.birth_date_range_year_only.upper is not None
            ):
                self.birth_date_range_year_only = NumericRange(
                    self.birth_date_range_year_only.upper,
                    self.birth_date_range_year_only.upper,
                    bounds="[]",
                )
            elif (
                self.birth_date_range_year_only.lower is not None
                and self.birth_date_range_year_only.upper is None
            ):
                self.birth_date_range_year_only = NumericRange(
                    self.birth_date_range_year_only.lower,
                    self.birth_date_range_year_only.lower,
                    bounds="[]",
                )
            else:
                self.birth_date_range_year_only = NumericRange(
                    self.birth_date_range_year_only.lower,
                    self.birth_date_range_year_only.upper,
                    bounds="[]",
                )
        if self.death_date_range_year_only:
            if (
                self.death_date_range_year_only.lower is None
                and self.death_date_range_year_only.upper is not None
            ):
                self.death_date_range_year_only = NumericRange(
                    self.death_date_range_year_only.upper,
                    self.death_date_range_year_only.upper,
                    bounds="[]",
                )
            elif (
                self.death_date_range_year_only.lower is not None
                and self.death_date_range_year_only.upper is None
            ):
                self.death_date_range_year_only = NumericRange(
                    self.death_date_range_year_only.lower,
                    self.death_date_range_year_only.lower,
                    bounds="[]",
                )
            else:
                self.death_date_range_year_only = NumericRange(
                    self.death_date_range_year_only.lower,
                    self.death_date_range_year_only.upper,
                    bounds="[]",
                )

    def __str__(self):
        if self.surname and self.given_name:
            return "{0}, {1} {2}".format(
                self.surname, self.given_name, self._get_life_span()
            )
        if self.given_name and not self.surname:
            return "{0} {1}".format(self.given_name, self._get_life_span())
        if self.surname and not self.given_name:
            return "{0} {1}".format(self.surname, self._get_life_span())

    def _get_life_span(self) -> str:
        birth_range = str(clean_range(self.birth_date_range_year_only))
        death_range = str(clean_range(self.death_date_range_year_only))
        if not birth_range and not death_range:
            return ""
        else:
            return (
                birth_range
                + "--"
                + death_range
            )

    def _get_work_contributions_by_role(self, role: str) -> QuerySet:
        return self.contributions_works.filter(role=role)

    def _get_works_by_role(self, role: str) -> QuerySet:
        musical_work_model = apps.get_model("database", "musicalwork")
        ids = set()
        contributions = self._get_work_contributions_by_role(role)
        for contribution in contributions:
            ids.add(contribution.contributed_to_work_id)
        works = musical_work_model.objects.filter(id__in=ids)
        return works

    @property
    def name(self) -> str:
        """Get print friendly version of this Person's name"""
        return self.given_name + " " + self.surname

    @property
    def date_of_birth(self) -> str:
        """Get a print friendly version of range_date_birth"""
        return str(self.birth_date_range_year_only)

    @property
    def date_of_death(self) -> str:
        """Get a print friendly version of range_date_death"""
        return str(self.death_date_range_year_only)

    @property
    def works_composed(self) -> QuerySet:
        """Get the MusicalWorks composed by this Person"""
        return self._get_works_by_role("COMPOSER")

    @property
    def works_arranged(self) -> QuerySet:
        """Get the MusicalWorks arranged by this Person"""
        return self._get_works_by_role("ARRANGER")

    @property
    def works_authored(self) -> QuerySet:
        """Get the MusicalWorks authored by this Person"""
        return self._get_works_by_role("AUTHOR")

    @property
    def works_transcribed(self) -> QuerySet:
        """Get the MusicalWorks transcribed by this Person"""
        return self._get_works_by_role("TRANSCRIBER")

    @property
    def works_improvised(self) -> QuerySet:
        """Get the MusicalWorks improvised by this Person"""
        return self._get_works_by_role("IMPROVISER")

    @property
    def works_performed(self) -> QuerySet:
        """Get the MusicalWorks performed by this Person"""
        return self._get_works_by_role("PERFORMER")
