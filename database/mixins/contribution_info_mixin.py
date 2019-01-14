"""Define a Mixin for models that use Contribution"""
from typing import List

from django.db.models import QuerySet

from database.models.geographic_area import GeographicArea
from database.models.person import Person


class ContributionInfoMixin(object):
    """A Mixin to be added to models that are related to Contribution.

    Provides methods to easily extract relevant information about all the
    Contributions related to the model.
    """

    def _get_contributions_by_role(self, role: str) -> QuerySet:
        return self.contributions.filter(role=role)

    def _get_persons_by_role(self, role: str) -> QuerySet:
        contributions = self._get_contributions_by_role(role)
        ids = []
        for contribution in contributions:
            ids.append(contribution.person_id)
        persons = Person.objects.filter(id__in=ids)
        return persons

    def _get_locations_by_role(self, role: str) -> QuerySet:
        contributions = self._get_contributions_by_role(role)
        ids = []
        for contribution in contributions:
            ids.append(contribution.location_id)
        locations = GeographicArea.objects.filter(id__in=ids)
        return locations

    def _get_dates_by_role(self, role: str) -> List[str]:
        contributions = self._get_contributions_by_role(role)
        dates = []
        for contribution in contributions:
            dates.append(contribution.date)
        return dates

    @property
    def composers(self) -> QuerySet:
        """Get the Persons that are contributed as Composers.

        Returns
        -------
        composers : QuerySet
            A QuerySet of Person objects
        """
        return self._get_persons_by_role('COMPOSER')

    @property
    def arrangers(self) -> QuerySet:
        """Get the Persons that are contributed as Arrangers.

        Returns
        -------
        arrangers : QuerySet
            A QuerySet of Person objects
        """
        return self._get_persons_by_role('ARRANGER')

    @property
    def authors(self) -> QuerySet:
        """Get the Persons that are contributed as Authors of Text.

        Returns
        -------
        authors : QuerySet
            A QuerySet of Person objects
        """
        return self._get_persons_by_role('AUTHOR')

    @property
    def transcribers(self) -> QuerySet:
        """Get the Persons that are contributed as Transcribers.

        Returns
        -------
        transcribers : QuerySet
            A QuerySet of Person objects
        """
        return self._get_persons_by_role('TRANSCRIBER')

    @property
    def improvisers(self) -> QuerySet:
        """Get the Persons that are contributed as Improvisers.

        Returns
        -------
        improvisers : QuerySet
            A QuerySet of Person objects
        """
        return self._get_persons_by_role('IMPROVISER')

    @property
    def performers(self) -> QuerySet:
        """Get the Persons that are contributed as Performers.

        Returns
        -------
        performers : QuerySet
            A QuerySet of Person objects
        """
        return self._get_persons_by_role('PERFORMER')

    @property
    def composers_dates(self) -> List[str]:
        """Get the dates of Contributions made by Composers.

        Returns
        -------
        dates : List[str]
            A list of date ranges represented as strings
        """
        return self._get_dates_by_role('COMPOSER')

    @property
    def arrangers_dates(self) -> List[str]:
        """Get the dates of Contributions made by Arrangers.

        Returns
        -------
        dates : List[str]
            A list of date ranges represented as strings
        """
        return self._get_dates_by_role('ARRANGER')

    @property
    def authors_dates(self) -> List[str]:
        """Get the dates of Contributions made by Authors of Text.

        Returns
        -------
        dates : List[str]
            A list of date ranges represented as strings
        """
        return self._get_dates_by_role('AUTHOR')

    @property
    def transcribers_dates(self) -> List[str]:
        """Get the dates of Contributions made by Transcribers.

        Returns
        -------
        dates : List[str]
            A list of date ranges represented as strings
        """
        return self._get_dates_by_role('TRANSCRIBER')

    @property
    def improvisers_dates(self) -> List[str]:
        """Get the dates of Contributions made by Improvisers.

        Returns
        -------
        dates : List[str]
            A list of date ranges represented as strings
        """
        return self._get_dates_by_role('IMPROVISER')

    @property
    def performers_dates(self) -> List[str]:
        """Get the dates of Contributions made by Performers.

        Returns
        -------
        dates : List[str]
            A list of date ranges represented as strings
        """
        return self._get_dates_by_role('PERFORMER')

    @property
    def composers_locations(self) -> QuerySet:
        """Get the locations of Contributions made by Composers.

        Returns
        -------
        locations : QuerySet
            A QuerySet of GeographicLocation objects
        """
        return self._get_locations_by_role('COMPOSER')

    @property
    def arrangers_locations(self) -> QuerySet:
        """Get the locations of Contributions made by Arrangers.

        Returns
        -------
        locations : QuerySet
            A QuerySet of GeographicLocation objects
        """
        return self._get_locations_by_role('ARRANGER')

    @property
    def authors_locations(self) -> QuerySet:
        """Get the locations of Contributions made by Authors of Text.

        Returns
        -------
        locations : QuerySet
            A QuerySet of GeographicLocation objects
        """
        return self._get_locations_by_role('AUTHOR')

    @property
    def transcribers_locations(self) -> QuerySet:
        """Get the locations of Contributions made by Transcribers.

        Returns
        -------
        locations : QuerySet
            A QuerySet of GeographicLocation objects
        """
        return self._get_locations_by_role('TRANSCRIBER')

    @property
    def improvisers_locations(self) -> QuerySet:
        """Get the locations of Contributions made by Improvisers.

        Returns
        -------
        locations : QuerySet
            A QuerySet of GeographicLocation objects
        """
        return self._get_locations_by_role('IMPROVISER')

    @property
    def performers_locations(self) -> QuerySet:
        """Get the locations of Contributions made by Performers.

        Returns
        -------
        locations : QuerySet
            A QuerySet of GeographicLocation objects
        """
        return self._get_locations_by_role('PERFORMER')

    @property
    def certainty_of_attributions(self) -> bool:
        """Get the certainty of all Contributions. True only if all are True."""
        certainties = self.contributions.values_list('certainty_of_attribution',
                                                     flat=True)
        if False in certainties:
            return False
        else:
            return True
