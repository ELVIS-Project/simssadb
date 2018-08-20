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

from database.models.musical_work import MusicalWork
from database.models.contributed_to import ContributedTo
from database.models.person import Person
from database.models.section import Section
from database.models.source import Source
from database.models.collection_of_sources import CollectionOfSources
from database.models.symbolic_music_file import SymbolicMusicFile
from database.models.genre import Genre
from database.models.part import Part
from database.models.instrument import Instrument

def parseSource(item_name, item_type):
    try:
        if item_type.__name__ == 'Section' or item_type.__name__ == 'CollectionOfSources':
            return item_type.objects.get(title=item_name)
        elif item_type.__name__ == 'Genre' or item_type.__name__ == 'Instrument':
            return item_type.objects.get(name=item_name)
    except item_type.DoesNotExist:
        print('Does not exist: ' + item_name)
        return None

def parseMusicalWork(item_name, surname_input, given_name_input):
    return MusicalWork.objects.filter(variant_titles__contains=[item_name], contributors__surname=surname_input, contributors__given_name=given_name_input)

def parseSection(musical_work_name, section_name, surname_input, given_name_input):
    return MusicalWork.objects.filter(variant_titles__contains=[musical_work_name], sections__title=section_name, contributors__surname=surname_input, contributors__given_name=given_name_input)

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

print('Adding musical works, sections, parts...')

with open(os.getcwd() + '/sample_data/elvisdb/work_section.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    
    for row in readCSV:
        collection_input = row[0]
        work_input = row[1]
        work_start_date_input = row[2]
        work_end_date_input = row[3]
        section_input = row[4]
        section_start_date_input = row[5]
        section_end_date_input = row[6]
        person_surname_input = row[7]
        person_given_name_input = row[8]
        genre_input = row[9]
        religiosity_input = row[10]
        part_list = [row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23]]

        collection = parseSource(collection_input, CollectionOfSources)
        
        if collection is not None:
            workQuery = parseMusicalWork(work_input, person_surname_input, person_given_name_input)
            person = parsePerson(person_surname_input, person_given_name_input)
            
            if not workQuery:
                work = MusicalWork(variant_titles=[work_input],
                                   sacred_or_secular=religiosity_input)
                work.save()

                if genre_input is not '':
                    genre = parseSource(genre_input, Genre)
                    work.genres_as_in_type.add(genre)
                    work.save()

                if person is not None:
                    contribute = ContributedTo(person=person, certain=True,
                                        role='COMPOSER',
                                        contributed_to_work=work)

                    if work_start_date_input:
                        contribute.date = (work_start_date_input, work_end_date_input)
                    else:
                        contribute.date = (None, work_end_date_input)

                    contribute.save()
            else:
                work = workQuery[0]

            if section_input is not '':
                sectionQuery = parseSection(work_input, section_input, person_surname_input, person_given_name_input)

                if not sectionQuery:
                    section = Section(title=section_input)
                    section.save()

                    work.sections.add(section)

                    if person is not None:
                        contribute = ContributedTo(person=person, certain=True,
                                            role='COMPOSER',
                                            contributed_to_section=section)
                        if section_start_date_input:
                            contribute.date = (section_start_date_input, section_end_date_input)
                        else:
                            contribute.date = (None, section_end_date_input)

                        contribute.save()

                    for part_input in part_list:
                        if part_input is not '':
                            instrument = parseSource(part_input, Instrument)
                            
                            if instrument is not None:
                                part = Part(label=part_input, in_section=section, written_for=instrument)
                                part.save()

                                if person is not None:
                                    contribute = ContributedTo(person=person, certain=True,
                                                        role='COMPOSER',
                                                        contributed_to_part=part)

                                    contribute.save()
