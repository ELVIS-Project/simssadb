import os
from django.test import TestCase
from django.core.files import File as PythonFile
from django.conf import settings
from database.models import *

# Create your tests here.

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
