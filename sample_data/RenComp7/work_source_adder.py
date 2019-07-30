import os
import sys
import re
from datetime import date
import csv

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
from database.models.part import Part
from database.models.software import Software
from database.models.encoding_workflow import EncodingWorkFlow
from database.models.instrument import Instrument
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.contribution_musical_work import ContributionMusicalWork
from database.models.contribution_section import ContributionSection
from database.models.genre_as_in_type import GenreAsInType
from database.models.source_instantiation import SourceInstantiation
from sample_data.Florence_164.work_source_adder import parseSource

def createContribution(p, work, section):
    """

    :return:
    """
    contribute = ContributionMusicalWork.objects.get_or_create(
        person=p,
        certainty_of_attribution=True,  # We assume these pieces are all secure
        role='COMPOSER',
        contributed_to_work=work
    )[0]
    # contribute.objects.get_or_create()

    contribute = ContributionSection.objects.get_or_create(
        person=p,
        certainty_of_attribution=True,
        role='COMPOSER',
        contributed_to_section=section
    )[0]
    return contribute


def addPiece(given_name_input, surname_input, birth_input, death_input, viaf_url_input, folder_name, counter, header):
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

    p = Person.objects.get_or_create(given_name=given_name_input, surname=surname_input)[0]

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
    for file_name_all in os.listdir(
            os.path.join(os.getcwd(), folder_name)):  # iterate each file within the folder
        print('-----------------------', given_name_input, surname_input, birth_input, death_input, viaf_url_input,
              folder_name, counter, header)
        counter += 1
        file_name, file_extension = os.path.splitext(file_name_all)
        all_file_names.append(file_name)
        if folder_name != 'Giovanni_Pierluigi_da_Palestrina':
            # continue
            file_name_split = file_name.split('-')
            if folder_name == 'Tomas_Luis_de_Victoria':
                file_name = file_name_split[0]
                section_name = file_name_split[1:]
            else:
                file_name = file_name_split[1]
                # different codes
                section_name = file_name_split[2:]
            file_name = file_name.replace('_', ' ')

            section_name_format = ' '.join(section_name)
            print('file name:', file_name)
            print('section name:', section_name_format)
            # if file_name == 'Confitebor tibi' and ('Kyrie' in section_name_format or section_name_format == ''):
            # print('debug')
        else:  # We need different schemes for Palestrina
            file_name_split = file_name.split('_')
            if any(word in file_name for word in ['(I)', '(II)', '(III)']):  # all these cases the last two are sections
                section_name_format = ' '.join(file_name_split[-2:])
                file_name = ' '.join(file_name_split[:-2])
            else:
                if any(word in file_name for word in
                       ['_I', '_II', '_III', '_rpt']):  # all these cases the three two are sections
                    section_name_format = ' '.join(file_name_split[-3:])
                    file_name = ' '.join(file_name_split[:-3])
                elif 'Gloria_of_1600_4' in file_name:
                    section_name_format = ' '.join(file_name_split[-4:])
                    file_name = ' '.join(file_name_split[:-4])
                else:
                    section_name_format = ' '.join(file_name_split[-2:])
                    file_name = ' '.join(file_name_split[:-2])
            print('file name:', file_name)
            print('section name:', section_name_format)
        section_name_format = re.sub(r'[0-9]+', '', section_name_format)
        # remove the unnecessary numbering for sections
        # Find the metadata in the CSV file
        with open(os.path.join(os.getcwd(), 'RenComp7_metadata_IL.csv')) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            rows = []
            for row in readCSV:
                rows.append(row)
        if rows[counter + 1][0] == os.path.join(folder_name,
                                               file_name_all):
            file_ID = counter + 1
        else:
            for file_ID, item in enumerate(rows[0]):
                if item == os.path.join(folder_name,
                                    file_name_all):
                    break
        file_name = rows[file_ID][3]
        section_name_format = rows[file_ID][4]
        if rows[file_ID][6] == 'Secular':
            religiosity_input = False
        elif rows[file_ID][6] == 'Sacred':
            religiosity_input = True
        else:
            religiosity_input = None
        genre_style_input = 'Renaissance'
        genre_type_input = rows[file_ID][5]
        # Save these info into the DB
        work, bool_work_new = MusicalWork.objects.get_or_create(
            variant_titles=[file_name],)
        composer = work.composers
        if composer.exists():
            if composer.values('given_name').get()['given_name'] != given_name_input or composer.values('surname').get()['surname'] != surname_input:
                work, bool_work_new = MusicalWork.objects.get_or_create(
                    variant_titles=[file_name + ' '], )  # non-intrusive name change for the musical works that share
                # the same name
        genre = parseSource(genre_style_input, GenreAsInStyle)
        work.genres_as_in_style.add(genre[0])
        genre = parseSource(genre_type_input, GenreAsInType)
        work.genres_as_in_type.add(genre[0])
        work._sacred_or_secular = religiosity_input
        work.save()
        if section_name_format == '':  # No section
            section, bool_section_new = Section.objects.get_or_create(title=file_name, musical_work=work)
        else:
            section, bool_section_new = Section.objects.get_or_create(title=section_name_format, musical_work=work)
        if bool_section_new == True:  # the sections do not exist
            contribute = createContribution(p, work, section)
        else:  # In case they both exist, create a new musical work for the new composer since their piece has the same
            # name
            if section_name_format == '':  # The same file name with no sections
                counter_same_file += 1

                work, bool_work_new = MusicalWork.objects.get_or_create(
                    variant_titles=[file_name_split[0][:-1] + ' ' + file_name],

                )
                section, bool_section_new = Section.objects.get_or_create(title=file_name_split[0][:-1] + file_name,
                                                                          musical_work=work)
            else:
                work, bool_work_new = MusicalWork.objects.get_or_create(
                    variant_titles=[file_name_split[0][:-1] + ' ' + file_name], )
                section, bool_section_new = Section.objects.get_or_create(title=section_name_format, musical_work=work)
            contribute = createContribution(p, work, section)
        # Create collections
        collection = CollectionOfSources.objects.get_or_create(title='RenComp7', url='https://www.google.ca')[0]
        source = Source.objects.get_or_create(
            collection=collection,
            portion=str(counter))[0]
        source_instantiation = SourceInstantiation.objects.get_or_create(source=source,
                                                                         )[0]
        source_instantiation.sections.add(section)
        file_path = os.path.join(os.getcwd(), folder_name, file_name_all)
        if file_extension == '.xml':
            file_local = open(file_path)
        else:
            file_local = open(file_path, 'rb')
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
                                    file_name_all), given_name_input, surname_input, file_name, section_name_format,
                       "RenComp7"])
    return counter, header

if __name__ == "__main__":
    print('Adding pieces for RenComp7...')

    mediatype = 'symbolic_music/'
    mediapath = getattr(settings, "MEDIA_ROOT", None)
    mediapath = mediapath + mediatype
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    counter = 0
    all_folders = os.listdir(os.path.join(os.getcwd()))
    # Create CSV file to export the metadata to check
    header = [
        ['File Name', 'Composer Given Name', 'Composer Surname', 'Musical Work Name', 'Section Name',
         'Collection Name'], ]

    for folder_name in all_folders:
        if folder_name == 'work_source_adder.py' or folder_name == '.DS_Store':
            continue
        else:
            if folder_name == 'Giovanni_Pierluigi_da_Palestrina':  # this one has different syntax
                given_name_input = 'Giovanni Pierluigi da'
                surname_input = 'Palestrina'
                birth_input = '1525'
                death_input = '1594'
                viaf_url_input = 'http://viaf.org/viaf/92280854'
            if folder_name == 'Johannes_Ockeghem':
                given_name_input = 'Johannes'
                surname_input = 'Ockeghem'
                birth_input = '1410'
                death_input = '1497'
                viaf_url_input = 'http://viaf.org/viaf/22150988'

            elif folder_name == 'Antoine_Busnoys':
                given_name_input = 'Antoine'
                surname_input = 'Busnoys'
                birth_input = '1430'
                death_input = '1492'
                viaf_url_input = ''  # I did not find VIAF entry for this one

            elif folder_name == 'Johannes_Martini':
                given_name_input = 'Johannes'
                surname_input = 'Martini'
                birth_input = '1440'
                death_input = '1497'
                viaf_url_input = 'http://viaf.org/viaf/66661850'

            elif folder_name == 'Josquin_des_Prez':
                given_name_input = 'des Prez'
                surname_input = 'Josquin'
                birth_input = '1440'
                death_input = '1521'
                viaf_url_input = 'http://viaf.org/viaf/100226284'
            elif folder_name == 'Pierre_de_la_Rue':
                given_name_input = 'Pierre de'
                surname_input = 'La Rue'
                birth_input = '1460'
                death_input = '1518'
                viaf_url_input = 'http://viaf.org/viaf/265244429'
            elif folder_name == 'Tomas_Luis_de_Victoria':
                given_name_input = 'Tomas Luis de'
                surname_input = 'Victoria'
                birth_input = '1548'
                death_input = '1611'
                viaf_url_input = 'http://viaf.org/viaf/32192606'

            counter, header = addPiece(given_name_input, surname_input, birth_input, death_input, viaf_url_input,
                                       folder_name, counter, header)

    with open(os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "sample_data", 'RenComp7_metadata.csv'), 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(header)
