import os
from django.test import TestCase
from django.core.files import File as PythonFile
from django.conf import settings
from django.core.exceptions import ValidationError
from model_bakery import baker
from database.models import *
from pprint import pprint
from psycopg2.extras import NumericRange
import random
import uuid


def gen_int_range() -> NumericRange:
    lower: int = random.randint(1400, 2001)
    upper: int = random.randint(lower + 1, (lower + 20))
    num_range = NumericRange(lower, upper, bounds="[)")
    return num_range


def random_str(length: int = 10) -> str:
    return uuid.uuid4().hex.upper()[0:length]


baker.generators.add(
    "django.contrib.postgres.fields.ranges.IntegerRangeField", gen_int_range
)


class ArchiveModelTest(TestCase):
    def setUp(self) -> None:
        sources = baker.make("Source", make_m2m=True, _quantity=5, _fill_optional=True)
        self.archive = baker.make("Archive", _fill_optional=True, sources=sources)

    def test_str(self) -> None:
        self.assertEqual(str(self.archive), self.archive.name)

    def test_get_absolute_url(self) -> None:
        self.assertEquals(
            self.archive.get_absolute_url(), f"/archives/{self.archive.id}"
        )


class ContributionMusicalWorkTest(TestCase):
    def setUp(self) -> None:
        person_birth_date = gen_int_range()
        person_death_date = NumericRange(
            person_birth_date.upper + 80, person_birth_date.upper + 85
        )
        contrib_date = NumericRange(
            person_birth_date.upper + 40, person_death_date.lower - 20
        )
        self.work = baker.make("MusicalWork", variant_titles=[random_str()])
        self.person = baker.make(
            "Person",
            _fill_optional=True,
            birth_date_range_year_only=person_birth_date,
            death_date_range_year_only=person_death_date,
        )
        self.contrib = baker.make(
            "ContributionMusicalWork",
            _fill_optional=True,
            person=self.person,
            date_range_year_only=contrib_date,
            contributed_to_work=self.work,
        )
        self.contrib_no_date = baker.make(
            "ContributionMusicalWork",
            date_range_year_only=None,
            contributed_to_work=self.work,
            person=self.person,
        )

    def test_str(self) -> None:
        person = str(self.contrib.person)
        role = self.contrib.role.lower()
        work = str(self.work)
        self.assertEquals(str(self.contrib), f"{person}, {role} of {work}")

    def test_date_property(self) -> None:
        lower: int = self.contrib.date_range_year_only.lower
        upper: int = self.contrib.date_range_year_only.upper
        self.assertEquals(self.contrib.date, f"({lower}-{upper-1})")
        self.assertEquals(self.contrib_no_date.date, "")

    def test_clean(self) -> None:
        person_birth_date = gen_int_range()
        person_death_date = NumericRange(
            person_birth_date.upper + 80, person_birth_date.upper + 85
        )
        contrib_date = NumericRange(
            person_birth_date.lower - 1, person_death_date.upper + 1
        )
        with self.assertRaisesMessage(
            ValidationError, "Date range is outside of contributor's life span"
        ):
            person = baker.make(
                "Person",
                _fill_optional=True,
                birth_date_range_year_only=person_birth_date,
                death_date_range_year_only=person_death_date,
            )
            baker.make(
                "ContributionMusicalWork",
                _fill_optional=True,
                person=person,
                date_range_year_only=contrib_date,
                contributed_to_work=self.work,
            )

    def test_get_absolute_url(self) -> None:
        self.assertEquals(
            self.contrib.get_absolute_url(), f"/contributions/{self.contrib.id}"
        )


class EncodingWorkflowModelTest(TestCase):
    def setUp(self) -> None:
        self.workflow = baker.make(
            "EncodingWorkflow",
            _create_files=True,
            _fill_optional=["encoder_names", "workflow_text", "workflow_file", "notes"],
        )
        self.workflow_w_sw = baker.make(
            "EncodingWorkflow",
            make_m2m=True,
            _fill_optional=["encoder_names", "encoding_software"],
        )

    def test_str(self) -> None:
        self.assertEquals(
            str(self.workflow), f"Encoded by: {self.workflow.encoder_names}"
        )
        # Test the __str__() method when the workflow has a software
        self.assertEquals(
            str(self.workflow_w_sw),
            f"Encoded by: {self.workflow_w_sw.encoder_names} with "
            f"{self.workflow_w_sw.encoding_software}",
        )

    def test_workflow_file_uploaded_correctly(self) -> None:
        path = os.path.join(settings.MEDIA_ROOT, self.workflow.workflow_file.name)
        self.assertEquals(path, self.workflow.workflow_file.path)

    def test_get_absolute_url(self) -> None:
        self.assertEquals(
            self.workflow.get_absolute_url(), f"/encodingworkflows/{self.workflow.id}"
        )

    def tearDown(self) -> None:
        """Delete the file that was uploaded when creating the test object"""
        os.remove(self.workflow.workflow_file.path)


class ExperimentalStudyModelTest(TestCase):
    def setUp(self) -> None:
        self.study = baker.make("ExperimentalStudy", _fill_optional=True)

    def test_str(self) -> None:
        self.assertEqual(str(self.study), self.study.title)

    def test_get_absolute_url(self) -> None:
        self.assertEquals(
            self.study.get_absolute_url(), f"/experimentalstudies/{self.study.id}"
        )


class ExtractedFeatureModelTest(TestCase):
    # TODO: fill this in
    pass


class FeatureFileModelTest(TestCase):
    # TODO: fill this in
    pass


class FeatureTypeModelTest(TestCase):
    # TODO: fill this in
    pass


class FileModelTest(TestCase):
    # TODO: fill this in
    pass


class GenreAsInStyleModelTest(TestCase):
    def setUp(self) -> None:
        self.style = baker.make("GenreAsInStyle", _fill_optional=True)

    def test_str(self) -> None:
        self.assertEqual(str(self.style), self.style.name)

    def test_get_absolute_url(self) -> None:
        self.assertEquals(self.style.get_absolute_url(), f"/styles/{self.style.id}")


class GenreAsInTypeModelTest(TestCase):
    def setUp(self) -> None:
        self.type = baker.make("GenreAsInType", _fill_optional=True)

    def test_str(self) -> None:
        self.assertEqual(str(self.type), self.type.name)

    def test_get_absolute_url(self) -> None:
        self.assertEquals(self.type.get_absolute_url(), f"/types/{self.type.id}")


class GeographicAreaModelTest(TestCase):
    def setUp(self) -> None:
        self.area = baker.make("GeographicArea", _fill_optional=True)
        self.works_list = [
            baker.make("MusicalWork", variant_titles=[random_str()]).id
            for x in range(5)
        ]
        self.works = MusicalWork.objects.filter(id__in=self.works_list)
        for i in range(5):
            baker.make(
                "ContributionMusicalWork",
                contributed_to_work=self.works[i],
                _fill_optional=True,
                location=self.area,
            )

    def test_str(self) -> None:
        self.assertEqual(str(self.area), self.area.name)

    def test_get_absolute_url(self) -> None:
        self.assertEquals(self.area.get_absolute_url(), f"/areas/{self.area.id}")

    def test_musical_works_property(self) -> None:
        self.assertQuerysetEqual(
            self.area.musical_works.all(),
            self.works,
            ordered=False,
            # The transform argument having the identity function is so the members of
            # the second QuerySet don't go through the repr() method, then we can
            # compare objects to objects
            transform=lambda x: x,
        )


class InstrumentModelTest(TestCase):
    def setUp(self) -> None:
        self.instrument = baker.make("Instrument", _fill_optional=True)
        self.work = baker.make("MusicalWork")
        self.section = baker.make("Section", musical_work=self.work)
        self.part_section = baker.make(
            "Part", section=self.section, written_for=self.instrument
        )
        self.part_musical_work = baker.make("Part")
        
    def test_str(self) -> None:
        self.assertEqual(str(self.instrument), self.instrument.name)

    def test_get_absolute_url(self) -> None:
        self.assertEquals(
            self.instrument.get_absolute_url(), f"/instruments/{self.instrument.id}"
        )


class LanguageModelTest(TestCase):
    def setUp(self) -> None:
        self.language = baker.make("Language", _fill_optional=True)

    def test_str(self) -> None:
        self.assertEqual(str(self.language), self.language.name)

    def test_get_absolute_url(self) -> None:
        self.assertEquals(
            self.language.get_absolute_url(), f"/languages/{self.language.id}"
        )


class MusicalWorkModelTest(TestCase):
    # TODO: fill this in
    pass


class PartModelTest(TestCase):
    # TODO: fill this in
    pass


class PersonModelTest(TestCase):
    # TODO: fill this in
    pass


class ResearchCorpusModelTest(TestCase):
    # TODO: fill this in
    pass


class SectionModelTest(TestCase):
    # TODO: fill this in
    pass


class SoftwareModelTest(TestCase):
    # TODO: fill this in
    pass


class SourceInstantiationModelTest(TestCase):
    # TODO: fill this in
    pass


class SourceModelTest(TestCase):
    # TODO: fill this in
    pass


class TypeOfSectionModelTest(TestCase):
    # TODO: fill this in
    pass


class ValidationWorkflowModelTest(TestCase):
    # TODO: fill this in
    pass
