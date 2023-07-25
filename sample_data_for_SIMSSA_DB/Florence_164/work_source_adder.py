import os
import sys
import csv
import fnmatch
from datetime import date
original_cwd = os.getcwd()  # change back to the original path for the next script

proj_path = "../../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
from django.conf import settings

application = get_wsgi_application()

from django.core.files import File as PythonFile

from database.models.musical_work import MusicalWork
from database.models.person import Person
from database.models.section import Section
from database.models.source import Source
from database.models.file import File
from database.models.part import Part
from database.models.software import Software
from database.models.encoding_workflow import EncodingWorkFlow
from database.models.instrument import Instrument
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.contribution_musical_work import ContributionMusicalWork
from database.models.genre_as_in_type import GenreAsInType
from database.models.source_instantiation import SourceInstantiation


def parseSource(item_name, item_type):
    try:
        if (item_type.__name__ == 'Section' or
                item_type.__name__ == 'Source'):

            return item_type.objects.get_or_create(title=item_name,
                                                   url='https://docs.google.com/spreadsheets/d/1G1CPeHKjLAIXZPJSuwIOOIoq9BiPm7H97ikBEZ9ayNE/edit#gid=588272074')

        elif (item_type.__name__ == 'GenreAsInStyle' or
              item_type.__name__ == 'Instrument' or
              item_type.__name__ == 'GenreAsInType'):

            return item_type.objects.get_or_create(name=item_name)

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
            return Person.objects.get_or_create(
                surname=surname_input,
                given_name=given_name_input
            )
        except Person.DoesNotExist:
            print('Does not exist: ' + surname_input)
            return None
    else:
        try:
            return Person.objects.get_or_create(surname='', given_name=given_name_input)
        except Person.DoesNotExist:
            print('Does not exist: ' + given_name_input)
            return None


def parseEncoder(software_input, text_input):
    if software_input is not '':
        try:
            software = Software.objects.get_or_create(name=software_input)[0]
            return EncodingWorkFlow.objects.get(software=software,
                                       work_flow_text=text_input)
        except EncodingWorkFlow.DoesNotExist:
            print('Does not exist: ' + software_input)
            return None
    else:
        return None


if __name__ == "__main__":
    print('Adding sources...')
    mediatype = 'symbolic_music/'
    mediapath = getattr(settings, "MEDIA_ROOT", None)
    mediapath = mediapath + mediatype
    print('os.getcwd', os.getcwd())
    with open(os.path.join(os.getcwd(), 'sample_data_for_SIMSSA_DB','Florence_164','Florence_metadata_SIMSSA_DB.csv')) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        for row in readCSV:
            collection_input = row[0]
            work_input = row[1]
            if row[7] == 'Secular':
                religiosity_input = False
            elif row[7] == 'Sacred':
                religiosity_input = True
            else:
                religiosity_input = None
            instrument_input = row[3]
            composer_given_name_input = row[4]
            composer_surname_input = row[5]
            if row[6] == '':
                composer_certainty_of_attribution = False
            else:
                composer_certainty_of_attribution = row[6]
            poet_given_name_input = row[11]
            poet_surname_input = row[12]
            if row[13] == '':
                poet_certainty_of_attribution = False
            else:
                poet_certainty_of_attribution = row[13]
            genre_style_input = row[8]
            genre_type_input = row[9]
            source_portion_input = row[10]
            file_type_input = ['xml', 'midi', 'pdf', 'sibelius']
            file_input = []
            print('portion', source_portion_input)
            file_type_input = ['xml', 'midi', 'pdf', 'sibelius']
            for folder_name in os.listdir(os.path.join(os.getcwd(), 'sample_data_for_SIMSSA_DB', 'Florence_164', 'files')):
                if folder_name == ".DS_Store":
                    continue
                for file_name in os.listdir(
                        os.path.join(os.getcwd(), 'sample_data_for_SIMSSA_DB', 'Florence_164', 'files', folder_name)):
                    if file_name == ".DS_Store":
                        continue
                    if int(float(source_portion_input)) < 10:
                        if '0' + str(int(float(source_portion_input))) in file_name:
                            file_input.append(file_name)
                    elif source_portion_input != '45.5':
                        if source_portion_input == '16.0':
                            if '16_' in file_name:
                                file_input.append(file_name)
                        elif source_portion_input == '64.0':
                            if '_64_' in file_name:
                                file_input.append(file_name)
                        elif str(int(float(source_portion_input))) in file_name \
                                and str(int(float(source_portion_input))) + '.' not in file_name:

                            file_input.append(file_name)
                    else:
                        if str(float(source_portion_input)) in file_name:
                            file_input.append(file_name)
            print('file_name', file_input)
            # url_input = [row[17], row[20], row[23]]

            collection = parseSource(collection_input, Source)

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
                )
                work.sacred_or_secular = religiosity_input
                work.save()

                # section = Section(title=work_input, musical_work=work)
                # section.save()

                instrument = parseSource(instrument_input, Instrument)
                part = None

                if instrument is not None:
                    part = Part(
                        musical_work=work,
                        written_for=instrument[0])
                    part.save()

                if genre_style_input is not '':
                    genre = parseSource(genre_style_input, GenreAsInStyle)
                    work.genres_as_in_style.add(genre[0])
                    work.save()

                if genre_type_input is not '':
                    genre = parseSource(genre_type_input, GenreAsInType)
                    work.genres_as_in_type.add(genre[0])
                    work.save()

                if composer is not None:
                    contribute = ContributionMusicalWork(
                        person=composer[0],
                        certainty_of_attribution=composer_certainty_of_attribution,
                        role='COMPOSER',
                        contributed_to_work=work
                    )
                    contribute.save()


                if poet is not None:
                    contribute = ContributionMusicalWork(
                        person=poet[0],
                        certainty_of_attribution=poet_certainty_of_attribution,
                        role='AUTHOR',
                        contributed_to_work=work
                    )
                    contribute.save()

                source = Source(
                    title=collection_input,
                    source_type='DIGITAL')
                source.save()

                source_instantiation = SourceInstantiation(source=source,
                                                           portion=source_portion_input, work=work)
                source_instantiation.save()
                work.save()
                for index, val in enumerate(file_type_input):
                    # Delete file if already exists
                    if not os.path.exists(mediapath):
                        os.makedirs(mediapath)
                    # for filename_media in os.listdir(mediapath):
                    #     if fnmatch.fnmatch(filename_media, file_input[index]):
                    #         os.remove(mediapath + filename_media)

                    file_path = os.getcwd()
                    file_path += '/sample_data_for_SIMSSA_DB/Florence_164/files/'
                    file_path += file_type_input[index]
                    file_path += '/'
                    for index2, val2 in enumerate(file_input):
                        if file_type_input[index] in val2 or (file_type_input[index] == 'midi' and 'mid' in val2) or (
                                file_type_input[index] == 'sibelius' and 'sib' in val2):
                            file_path += file_input[index2]
                            break

                    if file_type_input[index] == 'xml':
                        file_local = open(file_path)
                    else:
                        file_local = open(file_path, 'rb')

                    file_import = PythonFile(file_local)

                    symbolicfile = File(
                        file_type='sym',
                        instantiates=source_instantiation,
                        file=file_import,
                        file_format=file_type_input[index])
                    symbolicfile.file.name = file_input[index2]
                    symbolicfile.save()

                    file_import.closed
                    file_local.closed
    os.chdir(original_cwd)