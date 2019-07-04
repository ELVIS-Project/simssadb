from typing import List, Optional
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
    SymbolicMusicFile,
)


class FacetValue(object):
    def __init__(self, pk: int, display_name: str, count: int) -> None:
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
    def make_facet_values(self, ids: List[int]) -> List[FacetValue]:
        raise NotImplementedError

    facet_values: List[FacetValue] = []


