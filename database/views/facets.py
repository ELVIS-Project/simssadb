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

