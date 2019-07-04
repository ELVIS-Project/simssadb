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


