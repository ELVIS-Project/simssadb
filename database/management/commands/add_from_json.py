import json
from django.core.management.base import BaseCommand, CommandError
from database.models import File
from database.models import Section
from database.models import MusicalWork
from database.models import Part
from database.models import Source
from database.models import SourceInstantiation
from database.models import ContributionMusicalWork
from database.models import Person
from database.models import GeographicArea
from database.models import TypeOfSection
from database.models import GenreAsInStyle
from database.models import GenreAsInType
from database.models import Instrument
from typing import Union
from psycopg2.extras import NumericRange
from django.core.files import File as PythonFile

