import os
import sys
import csv
import fnmatch
from datetime import date

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
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.contribution import Contribution
from database.models.genre_as_in_type import GenreAsInType
from database.models.source_instantiation import SourceInstantiation


def parseSource(item_name, item_type):
    try:
        if (item_type.__name__ == 'Section' or
                item_type.__name__ == 'CollectionOfSources'):

            return item_type.objects.get(title=item_name)

        elif (item_type.__name__ == 'GenreAsInStyle' or
              item_type.__name__ == 'Instrument' or
              item_type.__name__ == 'GenreAsInType'):

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
            return Person.objects.filter(
                surname=surname_input,
                given_name=given_name_input
            ).first()
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
            software = Software.objects.get_or_create(name=software_input)[0]
            return Encoder.objects.get(software=software,
                                       work_flow_text=text_input)
        except Encoder.DoesNotExist:
            print('Does not exist: ' + software_input)
            return None
    else:
        return None


def createContribution(p, work, section):
    """

    :return:
    """
    contribute = Contribution.objects.get_or_create(
        person=p,
        certainty_of_attribution=True,  # We assume these pieces are all secure
        role='COMPOSER',
        contributed_to_work=work
    )[0]
    # contribute.objects.get_or_create()

    contribute = Contribution.objects.get_or_create(
        person=p,
        certainty_of_attribution=True,
        role='COMPOSER',
        contributed_to_section=section
    )[0]
    return contribute

def addPiece(given_name_input, surname_input, birth_input, death_input, viaf_url_input, folder_name, counter):
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
        p.range_date_birth = (None, birth_input + '-01-01')
    else:
        p.range_date_birth = None

    if death_input:
        p.range_date_death = (None, death_input + '-01-01')
    else:
        p.range_date_death = None

    if viaf_url_input:
        p.authority_control_url = viaf_url_input
    p.save()
    all_file_names = []

    counter_same_file= 1
    for file_name_all in os.listdir(
            os.path.join(os.getcwd(), 'sample_data', 'RenComp7', folder_name)):  # iterate each file within the folder
        counter += 1
        file_name, file_extension = os.path.splitext(file_name_all)
        all_file_names.append(file_name)
        file_name_split = file_name.split('-')
        if folder_name == 'Tomas_Luis_de_Victoria':
            file_name = file_name_split[0]
            section_name = file_name_split[1:]
        else:
            file_name = file_name_split[1]
            # different codes
            section_name = file_name_split[2:]
        file_name = file_name.replace('_', ' ')

        section_name_format = '_'.join(section_name)
        print('file name:', file_name)
        print('section name:', section_name_format)
        if file_name == 'Missa De beata virgine' and section_name_format == 'Kyrie':
            print('debug')

        # Save these info into the DB
        work, bool_work_new = MusicalWork.objects.get_or_create(
            variant_titles=[file_name],
        )
        # work.objects.get_or_create()
        if section_name_format == '':  # No section
            section, bool_section_new = Section.objects.get_or_create(title=file_name, musical_work=work)
        else:
            section, bool_section_new = Section.objects.get_or_create(title=section_name_format, musical_work=work)
        # section.objects.get_or_create()
        if bool_section_new == True :  # the sections do not exist
            contribute = createContribution(p, work, section)
        else :  # In case they both exist, create a new musical work for the new composer since their piece has the same
            # name
            if section_name_format == '':  # The same file name with no sections
                counter_same_file += 1

                work, bool_work_new = MusicalWork.objects.get_or_create(
                    variant_titles=[file_name_split[0][:-1] + ' ' + file_name],

                )
                section, bool_section_new = Section.objects.get_or_create(title=file_name_split[0][:-1] + file_name , musical_work=work)



            else:
                work, bool_work_new = MusicalWork.objects.get_or_create(
                    variant_titles=[file_name_split[0][:-1] + ' ' + file_name],

                )
                section, bool_section_new = Section.objects.get_or_create(title=section_name_format, musical_work=work)
            contribute = createContribution(p, work, section)
        # contribute.objects.get_or_create()
        # Create collections
        collection = CollectionOfSources.objects.get_or_create(title='RenComp7', url='https://www.google.ca')[0]
        source = Source.objects.get_or_create(
            collection=collection,
            portion=str(counter))[0]
        # source.objects.get_or_create()

        source_instantiation = SourceInstantiation.objects.get_or_create(source=source,
                                                                         )[0]
        source_instantiation.sections.add(section)
        # source_instantiation.objects.get_or_create()
        file_path = os.path.join(os.getcwd(), 'sample_data', 'RenComp7', folder_name, file_name_all)
        if file_extension == '.xml':
            file_local = open(file_path)
        else:
            file_local = open(file_path, 'rb')

        file_import = File(file_local)

        symbolicfile = SymbolicMusicFile(
            file_type=file_extension,
            manifests=source_instantiation,
            file=file_import,
            encoding_date=date.today())
        symbolicfile.file.name = file_name_all
        symbolicfile.save()

        file_import.closed
        file_local.closed
    return counter

print('Adding pieces for RenComp7...')

mediatype = 'symbolic_music/'
mediapath = getattr(settings, "MEDIA_ROOT", None)
mediapath = mediapath + mediatype
counter = 0
all_folders = os.listdir(os.path.join(os.getcwd(), 'sample_data', 'RenComp7'))
for folder_name in all_folders:

    if folder_name == 'Giovanni_Pierluigi_da_Palestrina':  # this one has different syntax
        given_name_input = 'Giovanni Pierluigi'
        surname_input = 'Da Palestrina'
        birth_input = '1525'
        death_input = '1594'
        viaf_url_input = 'http://viaf.org/viaf/92280854'
    elif folder_name == 'work_source_adder.py' or folder_name == '.DS_Store':
        continue
    else:
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
            given_name_input = 'Tomas Luis'
            surname_input = 'De Victoria'
            birth_input = '1548'
            death_input = '1611'
            viaf_url_input = 'http://viaf.org/viaf/32192606'
        counter = addPiece(given_name_input, surname_input, birth_input, death_input, viaf_url_input, folder_name, counter)

