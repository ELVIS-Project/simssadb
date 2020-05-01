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

    def create_contribution_from_dict(
        self, contribution_dict: dict, musical_work: MusicalWork
    ) -> ContributionMusicalWork:
        person = self.create_person_from_dict(contribution_dict["person"])
        location, created = GeographicArea.objects.get_or_create(
            name=contribution_dict["location"]
        )
        date_start = contribution_dict["date_start"]
        date_end = contribution_dict["date_end"]
        if date_start == date_end:
            date_end = date_end + 1
        if date_start > date_end:
            temp = date_start
            date_start = date_end
            date_end = temp
        date_range = NumericRange(date_start, date_end)

        contribution, created = ContributionMusicalWork.objects.get_or_create(
            person=person,
            location=location,
            certainty_of_attribution=contribution_dict["certainty"],
            role=contribution_dict["role"].upper(),
            date_range_year_only=date_range,
            contributed_to_work=musical_work,
        )

        return contribution

    def create_person_from_dict(self, person_dict: dict) -> Person:
        birth_location, created = GeographicArea.objects.get_or_create(
            name=person_dict["birth_location"]
        )
        death_location, created = GeographicArea.objects.get_or_create(
            name=person_dict["death_location"]
        )
        birth_date_start = person_dict["birth_date_start"]
        birth_date_end = person_dict["birth_date_end"]
        if birth_date_start == birth_date_end:
            birth_date_end = birth_date_end + 1
        if birth_date_start > birth_date_end:
            temp = birth_date_start
            birth_date_start = birth_date_end
            birth_date_end = temp
        birth_date_range = NumericRange(birth_date_start, birth_date_end)

        death_date_start = person_dict["death_date_start"]
        death_date_end = person_dict["death_date_end"]
        if death_date_start == death_date_end:
            death_date_end = death_date_end + 1
        if death_date_start > death_date_end:
            temp = death_date_start
            death_date_start = death_date_end
            death_date_end = temp
        death_date_range = NumericRange(death_date_start, death_date_end)

        person, created = Person.objects.get_or_create(
            given_name=person_dict["given_name"],
            surname=person_dict["surname"],
            authority_control_url=person_dict["authority_control_url"],
            birth_date_range_year_only=birth_date_range,
            death_date_range_year_only=death_date_range,
            birth_location=birth_location,
            death_location=death_location,
        )

        return person

    def create_section_from_dict(
        self, section_dict: dict, musical_work: MusicalWork
    ) -> Section:
        type_of_section, created = TypeOfSection.objects.get_or_crete(
            name=section_dict["type_of_section"]
        )
        section, created = Section.objects.get_or_create(
            title=section_dict["title"],
            musical_work=musical_work,
            ordering=section_dict["ordering"],
            type_of_section=type_of_section,
        )

        parts = section_dict["parts"]
        for part_dict in parts:
            self.create_part_from_dict(part_dict, section)

        return section
