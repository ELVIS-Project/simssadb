"""Defines a Person model"""
from django.apps import apps
from django.contrib.postgres.fields import IntegerRangeField
from django.db import models
from django.db.models import QuerySet, CheckConstraint, Q
from psycopg2.extras import NumericRange
from database.utils.model_utils import clean_range
from database.models.custom_base_model import CustomBaseModel


class Person(CustomBaseModel):
    """A person that contributed to a MusicalWork/Section/Part

    Attributes
    ----------
    given_name : models.CharField
        The given name of this Person

    surname : models.CharField
        The surname of this Person

    birth_date_range_year_only : IntegerRangeField   
        An integer range representing year range of the birth of this Person
        
        An integer range is used to allow for uncertain dates. The range thus represents
        a lower and upper bound on the years that this Person could have been born
        
        Ranges in PostgreSQL are standardized to a ``[)`` interval, that is closed on 
        the lower bound and open on the upper bound. 

        If the date of birth of the Person can be determined to one specific year, then 
        such year should be entered as the lower bound and the next year as the upper 
        bound (since the upper bound is open). For example, if the year is determined to 
        be 1750, the range should then be ``[1750, 1751)``.

        If the birth could have occurred between the years of 1749 and 1755, then
        the range should be ``[1749, 1756)`` to account for the open upper bound.

        Neither bound should be ``Null`` since PostgreSQL interprets those as infinity.

    death_date_range_year_only : IntegerRangeField
       An integer range representing year range of the death of this Person

       See birth_date_range_year_only for a more in depth explanation of integer ranges

    birth_location : models.ForeignKey
        Reference to the GeographicArea where this Person was born

    death_location : models.ForeignKey
        Reference to the GeographicArea where this Person died

    authority_control_url : models.URLField
        An URL linking to an authority control description of this Person

    contributions : models.fields.related_descriptors.ReverseManyToOneDescriptor
        References to the Contributions made by this Person
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
            #TODO: explain
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
            ),
        ]

    def clean(self) -> None:
        # TODO: refactor
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
            return birth_range + "--" + death_range

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
        """Get front-end friendly version of this Person's name
        
        Returns
        -------
        str
           Front-end friendly name
        """
        return self.given_name + " " + self.surname

    @property
    def date_of_birth(self) -> str:
        """Get a print friendly version of range_date_birth
        
        Returns
        -------
        str
            Front-end friendly date of birth
        """
        return str(self.birth_date_range_year_only)

    @property
    def date_of_death(self) -> str:
        """Get a print friendly version of range_date_death
        
        Returns
        -------
        str
            Front-end friendly date of death
        """
        return str(self.death_date_range_year_only)

    @property
    def works_composed(self) -> QuerySet:
        """Get the MusicalWorks composed by this Person
        
        Returns
        -------
        QuerySet
            QuerySet of Person objects
        """
        return self._get_works_by_role("COMPOSER")

    @property
    def works_arranged(self) -> QuerySet:
        """Get the MusicalWorks arranged by this Person
        
        Returns
        -------
        QuerySet
            QuerySet of Person objects
        """
        return self._get_works_by_role("ARRANGER")

    @property
    def works_authored(self) -> QuerySet:
        """Get the MusicalWorks authored by this Person

        Returns
        -------
        QuerySet
            QuerySet of Person objects
        """
        return self._get_works_by_role("AUTHOR")

    @property
    def works_transcribed(self) -> QuerySet:
        """Get the MusicalWorks transcribed by this Person
        
        Returns
        -------
        QuerySet
            QuerySet of Person objects
        """
        return self._get_works_by_role("TRANSCRIBER")

    @property
    def works_improvised(self) -> QuerySet:
        """Get the MusicalWorks improvised by this Person
        
        Returns
        -------
        QuerySet
            QuerySet of Person objects
        """
        return self._get_works_by_role("IMPROVISER")

    @property
    def works_performed(self) -> QuerySet:
        """Get the MusicalWorks performed by this Person
        
        Returns
        -------
        QuerySet
            QuerySet of Person objects
        """
        return self._get_works_by_role("PERFORMER")
