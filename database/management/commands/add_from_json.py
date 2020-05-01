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

    def add_data(self, data: dict):
        for musical_work in data["musical_works"]:
            work = self.create_musical_work_from_dict(musical_work)
            work.save()  # So it sends signal to update the search vector

    def create_musical_work_from_dict(self, musical_work_dict: dict) -> MusicalWork:
        work, created = MusicalWork.objects.get_or_create(
            variant_titles=musical_work_dict["variant_titles"],
            sacred_or_secular=musical_work_dict["sacred"],
        )

        styles = musical_work_dict["styles"]
        for style_str in styles:
            style, created = GenreAsInStyle.objects.get_or_create(name=style_str)
            style.musical_works.add(work)
            style.save()

        types_of_work = musical_work_dict["types_of_work"]
        for type_str in types_of_work:
            type_of_work, created = GenreAsInType.objects.get_or_create(name=type_str)
            type_of_work.musical_works.add(work)
            type_of_work.save()

        contributions = musical_work_dict["contributions"]
        for contribution in contributions:
            self.create_contribution_from_dict(contribution, work)

        sections = musical_work_dict["sections"]
        for section in sections:
            self.create_section_from_dict(section, work)

        parts = musical_work_dict["parts"]
        for part in parts:
            self.create_part_from_dict(part, work)

        files = musical_work_dict["files"]
        for file in files:
            self.create_file_from_dict(file, work)

        return work
