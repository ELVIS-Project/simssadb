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

# jrp = CollectionOfSources(title='Josquin Research Project',
#                           physical_or_electronic='e')
# jrp.save()
# opera = CollectionOfSources(title='Opera Omnia',
#                             publication_date=(None, '1989-01-01'),
#                             physical_or_electronic='p')
# opera.save()

def parseSource(item_name, item_type):
    try:
        if item_type.__name__ == 'MusicalWork':
            return item_type.objects.filter(variant_titles__contains=[item_name])
        elif item_type.__name__ == 'Section' or item_type.__name__ == 'CollectionOfSources':
            return item_type.objects.get(title=item_name)
    except item_type.DoesNotExist:
        print('Does not exist: ' + item_name)
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

with open(os.getcwd() + '/sample_data/elvisdb/work_section2.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    
    # pierre = Person.objects.get(names__contains=['La Rue, Pierre de'])
    # josquin = Person.objects.get(names__contains='{Josquin Des Prez}')

    for row in readCSV:
        collection_input = row[0]
        work_input = row[1]
        section_input = row[2]
        person_surname_input = row[3]
        person_given_name_input = row[4]

        # print('Collection: ' + collection_input + \
        #     ', Work: ' + work_input + \
        #     ', Section: ' + section_input + \
        #     ', Person Surname: ' + person_surname_input + \
        #     ', Person Given Name: ' + person_given_name_input)

        collection = parseSource(collection_input, CollectionOfSources)
        
        if collection is not None:
            workQuery = parseSource(work_input, MusicalWork)
            person = parsePerson(person_surname_input, person_given_name_input)
            
            if not workQuery:
                work = MusicalWork(variant_titles=[work_input])
                work.save()

                if person is not None:
                    contribute = ContributedTo(person=person, certain=True,
                                        role='COMPOSER',
                                        contributed_to_work=work)
                    contribute.save()
            else:
                work = workQuery[0];

            if section_input is not None:
                section = Section(title=section_input)
                section.save()

                work.sections.add(section)

                if person is not None:
                    contribute = ContributedTo(person=person, certain=True,
                                        role='COMPOSER',
                                        contributed_to_section=section)
                    contribute.save()






        # if row[0] == 'P. de la Rue':
        #     print('Composer is Pierre')
        #     title = row[2]
        #     s = Section(title=title)
        #     s.save()
        #     w = MusicalWork.objects.filter(variant_titles__contains=[row[1]])[0]
        #     w.sections.add(s)
        #     ctr = ContributedTo(person=pierre, certain=True,
        #                         role='COMPOSER',
        #                         contributed_to_section=s)
        #     ctr.save()

        #     source_title = row[1] + ' ' + row[2] + ' source'
        #     source = Source(title=source_title)
        #     if row[3] == 'JRP':
        #         source.part_of_collection = jrp
        #     if row[3] == 'Opera Omnia 1989':
        #         source.part_of_collection = opera
        #     source.save()
        #     source.work.add(w)
        #     source.section.add(s)
        #     source.save()
        #     if row[4]:
        #         file = SymbolicMusicFile(file_type='.sib', file_size=1000,
        #                                  encoding_date=date.today(),
        #                                  file=row[4], manifests=source,
        #                                  encoded_with_id=1)
        #         file.save()

        # if row[0] == 'Josquin Des Pres':
        #     print('Composer is Josquin')
        #     title = row[2]
        #     s = Section(title=title)
        #     s.save()
        #     w = MusicalWork.objects.filter(variant_titles__contains=[row[1]])[0]
        #     w.sections.add(s)
        #     ctr = ContributedTo(person=josquin, certain=True,
        #                         role='COMPOSER',
        #                         contributed_to_section=s)
        #     ctr.save()
        #     source_title = row[1] + ' ' + row[2] + ' source'
        #     source = Source(title=source_title)
        #     if row[3] == 'JRP':
        #         source.part_of_collection = jrp
        #     if row[3] == 'Opera Omnia 1989':
        #         source.part_of_collection = opera
        #     source.save()
        #     source.work.add(w)
        #     source.section.add(s)
        #     source.save()
        #     if row[4]:
        #         file = SymbolicMusicFile(file_type='.sib', file_size=1000,
        #                                  encoding_date=date.today(),
        #                                  file=row[4], manifests=source,
        #                                  encoded_with_id=1)
        #         file.save()
        # if row[0] == 'Josquin Des Pres (not secure)':
        #     print('Maybe Josquin???')
        #     title = row[2]
        #     s = Section(title=title)
        #     s.save()
        #     w = MusicalWork.objects.filter(variant_titles__contains=[row[1]])[0]
        #     w.sections.add(s)
        #     ctr = ContributedTo(person=josquin, certain=True,
        #                         role='COMPOSER',
        #                         contributed_to_section=s,
        #                         encoded_with_id=1)
        #     ctr.save()
        #     source_title = row[1] + ' ' + row[2] + ' source'
        #     source = Source(title=source_title)
        #     if row[3] == 'JRP':
        #         source.part_of_collection = jrp
        #     if row[3] == 'Opera Omnia 1989':
        #         source.part_of_collection = opera
        #     source.save()
        #     source.work.add(w)
        #     source.section.add(s)
        #     source.save()
        #     if row[4]:
        #         file = SymbolicMusicFile(file_type='.sib', file_size=1000,
        #                                  encoding_date=date.today(),
        #                                  file=row[4], manifests=source,
        #                                  encoded_with_id=1)
        #         file.save()

