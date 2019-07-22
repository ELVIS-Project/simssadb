from typing import List, Optional, Union
from abc import ABCMeta, abstractmethod
from django.db.models import Count, F, Q, QuerySet, Value, When
from database.models import (
    ExtractedFeature,
    FeatureType,
    GenreAsInStyle,
    GenreAsInType,
    Instrument,
    MusicalWork,
    Person,
    Section,
    File,
)


class FacetValue(object):
    def __init__(self, pk: Union[int, None], display_name: str, count: int) -> None:
        self.pk = pk
        self.display_name = display_name
        self.count = count


class Facet(metaclass=ABCMeta):
    def __init__(self, selected: List[str] = None) -> None:
        if selected is None:
            self.selected: List[str] = []
        else:
            self.selected = selected

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def display_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def lookup(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def make_facet_values(self, ids: List[int]) -> List[Optional[FacetValue]]:
        raise NotImplementedError

    facet_values: List[Optional[FacetValue]] = []


class TypeFacet(Facet):
    name = "types"
    display_name = "Genre (Type of Work)"
    lookup = "genres_as_in_type__pk"

    def make_facet_values(self, ids: List[int]) -> List[Optional[FacetValue]]:
        facet_values: List[Optional[FacetValue]] = []
        type_tuples = (
            GenreAsInType.objects.filter(musical_works__in=ids).annotate(
                count=Count("musical_works"), display_name=F("name")
            )
        ).values_list("pk", "display_name", "count")
        for type_tuple in type_tuples:
            facet_values.append(FacetValue(*type_tuple))
        return facet_values


class StyleFacet(Facet):
    name = "styles"
    display_name = "Genre (Type of Work)"
    lookup = "genres_as_in_type__pk"

    def make_facet_values(self, ids: List[int]) -> List[Optional[FacetValue]]:
        facet_values: List[Optional[FacetValue]] = []
        style_tuples = (
            GenreAsInStyle.objects.filter(musical_works__in=ids).annotate(
                count=Count("musical_works"), display_name=F("name")
            )
        ).values_list("pk", "display_name", "count")
        for style_tuple in style_tuples:
            facet_values.append(FacetValue(*style_tuple))
        return facet_values


class ComposerFacet(Facet):
    name = "composers"
    display_name = "Composer"
    lookup = "contributions__person__pk"

    def make_facet_values(self, ids: List[int]) -> List[Optional[FacetValue]]:
        facet_values: List[Optional[FacetValue]] = []
        composer_tuples = (
            Person.objects.filter(
                contributions_works__contributed_to_work__in=ids,
                contributions_works__role="COMPOSER",
            ).annotate(count=Count("contributions_works__contributed_to_work"))
        ).values_list("pk", "given_name", "surname", "count")
        for composer_tuple in composer_tuples:
            facet_value = FacetValue(
                pk=composer_tuple[0],
                display_name="{0}, {1}".format(composer_tuple[2], composer_tuple[1]),
                count=composer_tuple[3],
            )
            facet_values.append(facet_value)
        return facet_values


class InstrumentFacet(Facet):
    name = "instruments"
    display_name = "Instrument/Voice"
    lookup = "sections__parts__written_for__pk"

    def make_facet_values(self, ids: List[int]) -> List[Optional[FacetValue]]:
        facet_values: List[Optional[FacetValue]] = []
        instrument_tuples = (
            Instrument.objects.filter(parts__section__musical_work__in=ids).annotate(
                count=Count("parts__section__musical_work")
            )
        ).values_list("pk", "name", "count")
        for instrument_tuple in instrument_tuples:
            facet_values.append(FacetValue(*instrument_tuple))
        return facet_values


class FileFormatFacet(Facet):
    name = "file_formats"
    display_name = "File Format"
    lookup = "source_instantiations__manifested_by_sym_files__file_type"

    def make_facet_values(self, ids: List[int]) -> List[Optional[FacetValue]]:
        facet_values: List[Optional[FacetValue]] = []
        file_format_tuples = (
            File.objects.filter(
                Q(manifests__sections__musical_work__in=ids)
                | Q(manifests__work__in=ids)
            )
            .values_list("file_type")
            .annotate(display_name=F("file_type"), count=Count("file_type"))
        )
        for file_format_tuple in file_format_tuples:
            facet_values.append(FacetValue(*file_format_tuple))
        return facet_values


class SacredFacet(Facet):
    name = "sacred"
    display_name = "Sacred or Secular"
    lookup = "sacred_or_secular"

    def make_facet_values(self, ids: List[int]) -> List[Optional[FacetValue]]:
        aggregated_query = MusicalWork.objects.filter(id__in=ids).aggregate(
            trues=Count("sacred_or_secular", filter=Q(sacred_or_secular=True)),
            falses=Count("sacred_or_secular", filter=Q(sacred_or_secular=False)),
            nones=Count("sacred_or_secular", filter=Q(sacred_or_secular=None)),
        )

        trues: Optional[FacetValue] = None
        falses: Optional[FacetValue] = None
        nones: Optional[FacetValue] = None
        if aggregated_query["trues"] > 0:
            trues = FacetValue(
                pk=True, display_name="Sacred", count=aggregated_query["trues"]
            )
        if aggregated_query["falses"] > 0:
            falses = FacetValue(
                pk=False, display_name="Secular", count=aggregated_query["falses"]
            )
        if aggregated_query["nones"] > 0:
            nones = FacetValue(
                pk=None, display_name="Non-Applicable", count=aggregated_query["nones"]
            )
        facet_values = [trues, falses, nones]
        facet_values = [i for i in facet_values if i is not None]
        return facet_values
