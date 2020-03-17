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
