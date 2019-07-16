"""Define a Person model"""
from django.apps import apps
from django.contrib.postgres.fields import IntegerRangeField
from django.db import models
from django.db.models import QuerySet
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

    Person.published : models.ManyToOneRel
        References to the CollectionsOfSources published by this Person

    See Also
    --------
    database.models.CustomBaseModel
    database.models.GeographicArea
    database.models.Contribution
    database.models.CollectionOfSources
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
        return (
            str(clean_range(self.birth_date_range_year_only))
            + "--"
            + str(clean_range(self.death_date_range_year_only))
        )

    def _get_work_contributions_by_role(self, role: str) -> QuerySet:
        return self.contributions_works.filter(role=role)

    def _get_sections_contributions_by_role(self, role: str) -> QuerySet:
        return self.contributions_sections.filter(role=role)

    def _get_works_by_role(self, role: str) -> QuerySet:
        musical_work_model = apps.get_model("database", "musicalwork")
        ids = set()
        contributions = self._get_work_contributions_by_role(role)
        for contribution in contributions:
            ids.add(contribution.contributed_to_work_id)
        works = musical_work_model.objects.filter(id__in=ids)
        return works

    def _get_sections_by_role(self, role: str) -> QuerySet:
        section_model = apps.get_model("database", "section")
        ids = set()
        contributions = self._get_sections_contributions_by_role(role)
        for contribution in contributions:
            ids.add(contribution.contributed_to_section_id)
        sections = section_model.objects.filter(id__in=ids)
        return sections

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

    @property
    def sections_composed(self) -> QuerySet:
        """Get the Sections arranged by this Person"""
        return self._get_sections_by_role("COMPOSER")

    @property
    def sections_arranged(self) -> QuerySet:
        """Get the Sections arranged by this Person"""
        return self._get_sections_by_role("ARRANGER")

    @property
    def sections_authored(self) -> QuerySet:
        """Get the Sections authored by this Person"""
        return self._get_sections_by_role("AUTHOR")

    @property
    def sections_transcribed(self) -> QuerySet:
        """Get the Sections transcribed by this Person"""
        return self._get_sections_by_role("TRANSCRIBER")

    @property
    def sections_improvised(self) -> QuerySet:
        """Get the Sections improvised by this Person"""
        return self._get_sections_by_role("IMPROVISER")

    @property
    def sections_performed(self) -> QuerySet:
        """Get the Sections performed by this Person"""
        return self._get_sections_by_role("PERFORMER")
