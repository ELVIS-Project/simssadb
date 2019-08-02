import os
import sys
import csv
from datetime import date
import re
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
from database.models.collection_of_sources import CollectionOfSources
from database.models.file import File
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.genre_as_in_type import GenreAsInType
from database.models.source_instantiation import SourceInstantiation
from sample_data.RenComp7.work_source_adder import createContribution
from sample_data.Florence_164.work_source_adder import parseSource



def addPiece(
        given_name_input,
        surname_input,
        birth_input,
        death_input,
        viaf_url_input,
        folder_name,
        counter,
        secure,
        header
):
    """

    :param given_name_input:
    :param surname_input:
    :param birth_input:
    :param death_input:
    :param viaf_url_input:
    :param folder_name:
    :return:
    """
    # create entries for the composer
    p = Person.objects.get_or_create(
        given_name=given_name_input, surname=surname_input
    )[0]

    if surname_input:
        p.surname = surname_input

    if birth_input:
        p.birth_date_range_year_only = (None, int(birth_input))
    else:
        p.birth_date_range_year_only = None

    if death_input:
        p.death_date_range_year_only = (None, int(death_input))
    else:
        p.death_date_range_year_only = None

    if viaf_url_input:
        p.authority_control_url = viaf_url_input
    p.save()
    all_file_names = []

    counter_same_file = 1
    for each_format in os.listdir(
            os.path.join(os.getcwd(), folder_name)
    ):  # iterate each file within the folder

        if each_format != ".DS_Store":
            for file_name_all in os.listdir(
                    os.path.join(
                        os.getcwd(), folder_name, each_format
                    )
            ):
                if os.path.isdir(file_name_all):
                    continue
                if file_name_all == ".DS_Store" or 'all duos' in file_name_all:
                    continue
                print("current file name is:", file_name_all)
                counter += 1
                file_name, file_extension = os.path.splitext(file_name_all)
                if file_extension == "":
                    continue
                all_file_names.append(file_name)
                if "-" in file_name_all:  # If there is a section
                    file_name_split = file_name.split("-")
                    if len(file_name_split) >= 3:  # Exception
                        file_name = file_name_split[0]
                        section_name = " ".join(file_name_split[1:])
                    else:

                        file_name = " ".join(file_name_split[:-1])
                        section_name = file_name_split[-1]
                else:  # No section
                    section_name = ""
                file_name = file_name.replace("_", " ")
                file_name = file_name.replace("Josquin", " ")
                file_name = file_name.replace("La Rue", " ")
                file_name = (
                    file_name.lower()
                )  # Remove the variants of inconsistent upper/lower cases
                file_name = file_name.strip()  # Remove the space
                file_name = (
                    file_name.capitalize()
                )  # Capitalize the first letter of the title
                print("file name:", file_name)
                print("section name:", section_name)
                section_name = section_name.strip()
                section_name = re.sub(' +', ' ', section_name)  # remove non-usable space
                if 'ista est' in file_name:
                    print('debug')
                # Find the metadata in the CSV file
                with open(os.path.join(os.getcwd(), 'JLSDD (corr IL).csv')) as csvfile:
                    readCSV = csv.reader(csvfile, delimiter=',')
                    rows = []
                    for row in readCSV:
                        rows.append(row)
                for each_row in rows:
                    if 'ista est' in file_name:
                        file_name_compare = file_name.replace('Credo ', '').replace('playne', '').replace('ferrarie', 'Ferrariae').replace('Ferrarie', 'Ferrariae').replace('sanctissuma', 'sanctissima').replace('Misse', 'Missa').lower()
                    else:
                        file_name_compare = file_name.replace('Credo ', '').replace('playne', '').replace('ferrarie', 'Ferrariae').replace('Ferrarie', 'Ferrariae').replace('est', 'es').replace('sanctissuma', 'sanctissima').replace('Misse', 'Missa').lower()
                    file_name_csv = each_row[2].replace('’', ' ').replace('é', 'e').lower()
                    file_name_csv = re.sub(' +', ' ', file_name_csv)
                    if file_name_compare in file_name_csv or file_name_csv in file_name_compare:
                        if section_name.replace(' (sounding correct)', '').replace(' 2 2', '').replace('In nomie', 'In nomine').lower() in each_row[3].replace('(', '').replace(')', '').lower():
                            if given_name_input.lower() in each_row[0].lower() and surname_input.lower() in each_row[1].lower():

                                print('match!')
                                file_name = each_row[2]
                                section_name = each_row[3]
                                collection = CollectionOfSources.objects.get_or_create(
                                    title=each_row[7])[0]
                                source = Source.objects.get_or_create(
                                    collection=collection, portion=str(counter)
                                )[0]
                                source_instantiation = SourceInstantiation.objects.get_or_create(
                                    source=source
                                )[0]
                            else:

                                print('not match?')
                        else:
                            print('file name from folder', file_name_compare)
                            print('file name from csv', file_name_csv)
                            print('composer name from folder', given_name_input)
                            print('composer name from csv', each_row[0])
                            print('section name from folder', section_name)
                            print('section name from csv', each_row[3])
                            print('not match?')
                # Save these info into the DB
                work, bool_work_new = MusicalWork.objects.get_or_create(
                    variant_titles=[file_name]
                )
                if section_name == "":  # No section
                    section, bool_section_new = Section.objects.get_or_create(
                        title=file_name, musical_work=work
                    )
                else:
                    section, bool_section_new = Section.objects.get_or_create(
                        title=section_name, musical_work=work
                    )
                if bool_section_new == True:  # the sections do not exist
                    contribute = createContribution(p, work, section)
                else:  # In case they both exist, create a new musical work for the new composer since their piece has the same
                    # name
                    if section_name == "":  # The same file name with no sections
                        counter_same_file += 1

                        work, bool_work_new = MusicalWork.objects.get_or_create(
                            variant_titles=[file_name]
                        )
                        section, bool_section_new = Section.objects.get_or_create(
                            title=file_name, musical_work=work
                        )
                    else:
                        work, bool_work_new = MusicalWork.objects.get_or_create(
                            variant_titles=[file_name]
                        )
                        section, bool_section_new = Section.objects.get_or_create(
                            title=section_name, musical_work=work
                        )

                    contribute = createContribution(p, work, section)
                # Create collections
                genre_style_input = 'Renaissance'
                genre_type_input = 'Mass'
                genre = parseSource(genre_style_input, GenreAsInStyle)
                work.genres_as_in_style.add(genre[0])
                genre = parseSource(genre_type_input, GenreAsInType)
                work.genres_as_in_type.add(genre[0])
                work.sacred_or_secular = True  # This dataset contains all religious pieces
                work.save()
                source_instantiation.sections.add(section)
                file_path = os.path.join(
                    os.getcwd(),
                    folder_name,
                    each_format,
                    file_name_all,
                )
                if file_extension == ".xml":
                    file_local = open(file_path)
                else:
                    file_local = open(file_path, "rb")
                file_import = PythonFile(file_local)
                symbolicfile = File(
                    file_type='sym',
                    instantiates=source_instantiation,
                    file=file_import,
                    file_format=file_extension)
                symbolicfile.file.name = file_name_all
                symbolicfile.save()
                file_import.closed
                file_local.closed
                header.append([os.path.join(folder_name,
                                            each_format,
                                            file_name_all), given_name_input, surname_input, file_name, section_name,
                               secure, "JLSDD"])
    return counter, header


print("Adding pieces for JLSDD...")

mediatype = "symbolic_music/"
mediapath = getattr(settings, "MEDIA_ROOT", None)
mediapath = mediapath + mediatype
counter = 0
os.chdir(os.path.dirname(os.path.abspath(__file__)))
all_folders = os.listdir(os.getcwd())
# Create CSV file to export the metadata to check
header = [
    ['File Name', 'Composer Given Name', 'Composer Surname', 'Musical Work Name', 'Section Name', 'Secure Attribution',
     'Collection Name'], ]

for folder_name in all_folders:
    if os.path.isfile(folder_name) or folder_name == "work_source_adder.py" or '(not secure)' in folder_name:
        continue

    else:
        print('the current folder is---------------------------------', folder_name)
        if "Josquin" in folder_name:  # this one has different syntax
            given_name_input = "Josquin"
            surname_input = "des Prez"
            birth_input = "1440"
            death_input = "1521"
            viaf_url_input = "http://viaf.org/viaf/100226284"
            if "(secure)" in folder_name:

                secure = True
            else:
                secure = False
        if "La Rue" in folder_name:
            given_name_input = "Pierre"
            surname_input = "La Rue"
            birth_input = "1460"
            death_input = "1518"
            viaf_url_input = "http://viaf.org/viaf/265244429"
            if "(secure)" in folder_name:
                secure = True
            else:
                secure = False
        counter, header = addPiece(
            given_name_input,
            surname_input,
            birth_input,
            death_input,
            viaf_url_input,
            folder_name,
            counter,
            secure,
            header
        )
# with open(os.path.join(os.getcwd(), "sample_data", 'JLSDD_metadata.csv'), 'w') as csvFile:
#     writer = csv.writer(csvFile)
#     writer.writerows(header)
