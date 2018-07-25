import os
import sys
import csv
from datetime import date

proj_path = "../../"

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
from database.models.instrument import Instrument
from database.models.genre import Genre
from database.models.contributed_to import ContributedTo


def parseSource(item_name, item_type):
    try:
        if (item_type.__name__ == 'Section' or
                item_type.__name__ == 'CollectionOfSources'):

            return item_type.objects.get(title=item_name)

        elif (item_type.__name__ == 'Genre' or
                item_type.__name__ == 'Instrument'):

            return item_type.objects.get(name=item_name)

    except item_type.DoesNotExist:
        print('Does not exist: ' + item_name)
        return None


def parseMusicalWork(item_name, surname_input, given_name_input):
    return MusicalWork.objects.filter(
        variant_titles__contains=[item_name],
        contributors__surname=surname_input,
        contributors__given_name=given_name_input
    )


def parseSection(section_name, work):
    try:
        return Section.objects.get(title=section_name, in_works=work)
    except Section.DoesNotExist:
        print('Does not exist: ' + section_name)
        return None


def parsePerson(surname_input, given_name_input):
    if surname_input is not '':
        try:
            return Person.objects.get(
                surname=surname_input,
                given_name=given_name_input
            )
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
    if software_input is not '':
        try:
            software = Software.objects.get(name=software_input)
            return Encoder.objects.get(
                software=software,
                work_flow_text=text_input
            )
        except Encoder.DoesNotExist:
            print('Does not exist: ' + software_input)
            return None
    else:
        return None


print('Adding sources...')

with open(os.getcwd() + '/sample_data/madrigal/work_source.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    for row in readCSV:
        collection_input = row[0]
        work_input = row[1]
        religiosity_input = row[2]
        instrument_input = row[3]
        composer_given_name_input = row[4]
        composer_surname_input = row[5]
        composer_certain = row[6]
        poet_given_name_input = row[7]
        poet_surname_input = row[8]
        poet_certain = row[9]
        genre_style_input = row[10]
        genre_type_input = row[11]
        source_portion_input = row[12]
        encoder_software_input = row[13]
        encoder_text_input = row[14]
        file_type_input = [row[15], row[18], row[21]]
        file_input = [row[16], row[19], row[22]]
        url_input = [row[17], row[20], row[23]]

        collection = parseSource(collection_input, CollectionOfSources)

        if collection is not None:

            composer = parsePerson(
                composer_surname_input,
                composer_given_name_input
            )

            if poet_given_name_input is not '':
                poet = parsePerson(poet_surname_input, poet_given_name_input)
            else:
                poet = None

            work = MusicalWork(
                variant_titles=[work_input],
                religiosity=religiosity_input
            )

            work.save()

            section = Section(title=work_input)
            section.save()
            work.sections.add(section)

            instrument = parseSource(instrument_input, Instrument)

            if instrument is not None:
                part = Part(
                    label=instrument_input,
                    in_section=section,
                    written_for=instrument
                )
                part.save()

            if genre_style_input is not '':
                genre = parseSource(genre_style_input, Genre)
                work.genres_as_in_style.add(genre)
                work.save()

            if genre_type_input is not '':
                genre = parseSource(genre_type_input, Genre)
                work.genres_as_in_type.add(genre)
                work.save()

            if composer is not None:
                contribute = ContributedTo(
                    person=composer,
                    certain=composer_certain,
                    role='COMPOSER',
                    contributed_to_work=work
                )
                contribute.save()

                contribute = ContributedTo(
                    person=composer,
                    certain=composer_certain,
                    role='COMPOSER',
                    contributed_to_section=section
                )
                contribute.save()

                contribute = ContributedTo(
                    person=composer,
                    certain=composer_certain,
                    role='COMPOSER',
                    contributed_to_part=part
                )
                contribute.save()

            if poet is not None:
                contribute = ContributedTo(
                    person=poet,
                    certain=poet_certain,
                    role='AUTHOR',
                    contributed_to_work=work
                )
                contribute.save()

                contribute = ContributedTo(
                    person=composer,
                    certain=composer_certain,
                    role='AUTHOR',
                    contributed_to_section=section
                )
                contribute.save()

                contribute = ContributedTo(
                    person=composer,
                    certain=composer_certain,
                    role='AUTHOR',
                    contributed_to_part=part
                )
                contribute.save()

            source = Source(
                        work=work,
                        part_of_collection=collection,
                        portion=source_portion_input
                    )

            source.save()
            source.sections.add(section)
            source.parts.add(part)
            source.save()

            encoder = parseEncoder(encoder_software_input, encoder_text_input)
            if encoder is not None:
                for index, val in enumerate(file_type_input):
                    file_path = os.getcwd()
                    file_path += '/sample_data/madrigal/files/'
                    file_path += file_type_input[index]
                    file_path += '/'
                    file_path += file_input[index]

                    if file_type_input[index] == 'xml':
                        file_local = open(file_path)
                    else:
                        file_local = open(file_path, 'rb')

                    file_import = File(file_local)

                    symbolicfile = SymbolicMusicFile(
                        file_type=file_type_input[index],
                        manifests=source,
                        file=file_import,
                        encoded_with=encoder
                    )
                    symbolicfile.file.name = file_input[index]
                    symbolicfile.save()

                    file_import.closed
                    file_local.closed
