import os
from django.test import TestCase
from django.core.files import File as PythonFile
from django.conf import settings
from model_bakery import baker
from database.models import *
from pprint import pprint
from psycopg2.extras import NumericRange
import random


def gen_int_range() -> NumericRange:
    lower: int = random.randint(1400, 2001)
    upper: int = random.randint(lower + 1, (lower + 20))
    num_range = NumericRange(lower, upper, bounds="[)")
    return num_range


baker.generators.add(
    "django.contrib.postgres.fields.ranges.IntegerRangeField", gen_int_range
)


class ArchiveModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Archive.objects.create(name="Test Archive", url="https://testarchive.com")

    def test_str(self) -> None:
        archive = Archive.objects.first()
        self.assertEqual(str(archive), "Test Archive")

    def test_get_absolute_url(self) -> None:
        archive = Archive.objects.get(id=1)
        self.assertEquals(archive.get_absolute_url(), f"/archives/{archive.id}")


class ContributionMusicalWorkTest(TestCase):
    # TODO: fill this in
    pass


class EncodingWorkflowTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        test_file = PythonFile(
            open("database/tests/test_file.txt"), name="test_file.txt"
        )
        EncodingWorkFlow.objects.create(
            encoder_names="Tester1, Tester2",
            workflow_text="Test workflow",
            workflow_file=test_file,
            notes="Test notes",
        )
        test_file.close()
        Software.objects.create(name="Test Software")

    def test_str(self) -> None:
        workflow = EncodingWorkFlow.objects.first()
        self.assertEquals(str(workflow), "Encoded by: Tester1, Tester2")

        # Test the __str__() method when the workflow has a software
        workflow.encoding_software = Software.objects.first()
        workflow.save()
        self.assertEquals(
            str(workflow),
            f"Encoded by: Tester1, Tester2 with {workflow.encoding_software}",
        )

    def test_workflow_file_uploaded_correctly(self) -> None:
        workflow = EncodingWorkFlow.objects.first()
        path = settings.MEDIA_ROOT + "workflows/test_file.txt"
        self.assertEquals(path, workflow.workflow_file.path)

    def test_get_absolute_url(self) -> None:
        workflow = EncodingWorkFlow.objects.get(id=1)
        self.assertEquals(
            workflow.get_absolute_url(), f"/encodingworkflows/{workflow.id}"
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Delete the file that was uploaded when creating the test object"""
        os.remove(EncodingWorkFlow.objects.first().workflow_file.path)
        super().tearDownClass()


class ExperimentalStudyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        corpus = ResearchCorpus.objects.create(title="Test Research Corpus")
        ExperimentalStudy.objects.create(
            title="Test Experimental Study",
            link="https://testexperimentalstudy.com",
            research_corpus_used=corpus,
            authors="Tester1, Tester2"
        )

    def test_str(self) -> None:
        experimentalstudy = ExperimentalStudy.objects.first()
        self.assertEqual(str(experimentalstudy), "Test Experimental Study")

    def test_get_absolute_url(self) -> None:
        experimentalstudy = ExperimentalStudy.objects.get(id=1)
        self.assertEquals(
            experimentalstudy.get_absolute_url(),
            f"/experimentalstudies/{experimentalstudy.id}",
        )


class ExtractedFeatureWorkModelTest(TestCase):
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
    @classmethod
    def setUpTestData(cls) -> None:
        GenreAsInStyle.objects.create(name="Test Style")

    def test_str(self) -> None:
        style = GenreAsInStyle.objects.first()
        self.assertEqual(str(style), "Test Style")

    def test_get_absolute_url(self) -> None:
        style = GenreAsInStyle.objects.first()
        self.assertEquals(style.get_absolute_url(), f"/styles/{style.id}")
