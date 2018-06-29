import os, sys

proj_path = "../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from database.models.musical_work import MusicalWork
from database.models.person import Person
from database.models.section import Section
from database.models.collection_of_sources import CollectionOfSources
from database.models.instrument import Instrument
from database.models.genre import Genre

print('Cleaning sections...')
Section.objects.all().delete()

print('Cleaning musical works...')
MusicalWork.objects.all().delete()

print('Cleaning collections...')
CollectionOfSources.objects.all().delete()

print('Cleaning genres...')
Genre.objects.all().delete()

print('Cleaning instruments...')
Instrument.objects.all().delete()

print('Cleaning persons...')
Person.objects.all().delete()



