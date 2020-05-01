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

class Command(BaseCommand):
    help = "Adds data from a JSON file (that conforms to the template) to the database"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str)

    def handle(self, *args, **options):
        file_path = options["json_file"]
        try:
            with open(file_path) as json_file:
                data = json.load(json_file)
                self.add_data(data)
        except FileNotFoundError:
            raise CommandError(f"The file {file_path} cannot be found")

