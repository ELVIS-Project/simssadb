import os, sys, csv
from datetime import date

proj_path = "../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.core.files import File

from database.models.musical_work import MusicalWork
from database.models.person import Person
from database.models.section import Section
from database.models.source import Source
from database.models.collection_of_sources import CollectionOfSources
from database.models.symbolic_music_file import SymbolicMusicFile
from database.models.part import Part
from database.models.software import Software
from database.models.encoder import Encoder

def parseSource(item_name, item_type):
    try:
        if item_type.__name__ == 'Section' or item_type.__name__ == 'CollectionOfSources':
            return item_type.objects.get(title=item_name)
        elif item_type.__name__ == 'GenreAsInStyle' or item_type.__name__ == 'Instrument':
            return item_type.objects.get(name=item_name)
    except item_type.DoesNotExist:
        print('Does not exist: ' + item_name)
        return None

def parseMusicalWork(item_name, surname_input, given_name_input):
    return MusicalWork.objects.filter(variant_titles__contains=[item_name], contributors__surname=surname_input, contributors__given_name=given_name_input)

def parseSection(section_name, work):
    try:
        return Section.objects.get(title=section_name, in_works=work)
    except Section.DoesNotExist:
        print('Does not exist: ' + section_name)
        return None

def parsePerson(surname_input, given_name_input):
    if surname_input is not '':
        try:
            return Person.objects.get(surname=surname_input, given_name=given_name_input)
        except Person.DoesNotExist:
            print('Does not exist: ' + surname_input)
            return None
    else:
        try:
            return Person.objects.get(surname='', given_name=given_name_input)
        except Person.DoesNotExist:
            print('Does not exist: ' + given_name_input)
            return None

def parseEncoder(software_input, text_input):
    try:
        software = Software.objects.get(name=software_input)
        return Encoder.objects.get(software=software, work_flow_text = text_input)
    except Encoder.DoesNotExist:
        print('Does not exist: ' + software_input)
        return None

print('Adding sources...')

with open(os.getcwd() + '/sample_data/elvisdb/source.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    
    for row in readCSV:
        collection_input = row[0]
        person_surname_input = row[1]
        person_given_name_input = row[2]
        work_input = row[3]
        section_input = row[4]
        url_input = row[5]
        file_input = row[6]
        encoder_software_input = row[7]
        encoder_text_input = row[8]

        collection = parseSource(collection_input, CollectionOfSources)
        person = parsePerson(person_surname_input, person_given_name_input)
        workQuery = parseMusicalWork(work_input, person_surname_input, person_given_name_input)
        encoder = parseEncoder(encoder_software_input, encoder_text_input)
        
        if workQuery:
            work = workQuery[0]
            section = parseSection(section_input, work)

            if section is not None:
                parts = section.parts.all()

                source = Source(work=work, part_of_collection=collection, url=url_input)
                source.save()
                source.sections.add(section)
                source.parts.set(parts)
                source.save()

                file_local = open(os.getcwd() + '/sample_data/elvisdb/files/' + file_input)
                file_import = File(file_local)

                symbolicfile = SymbolicMusicFile(manifests=source, file=file_import, encoded_with=encoder)
                symbolicfile.file.name = file_input
                symbolicfile.save()

                file_import.closed
                file_local.closed
        else:
            print('Does not exist: ' + work_input)