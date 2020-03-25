import os
from django.test import TestCase
from django.core.files import File as PythonFile
from django.conf import settings
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
    # TODO: fill this in
    pass


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
            baker.make("MusicalWork", variant_titles=[uuid.uuid4().hex.upper()[0:6]]).id
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
            # This is so the members of the second QuerySet don't go through the
            # repr() method, then we can compare objects to objects
            transform=lambda x: x,
        )


class InstrumentModelTest(TestCase):
    # TODO: fill this in
    pass



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
