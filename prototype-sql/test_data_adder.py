import prototype_sql as pt
import pandas as pd

pt.db_initialize()
df = pd.read_csv('/Users/gustavo/Development/SIMSSA-database/test-data/Josquin + La Rue Mass duos '
                 'Inventory - Sheet1.csv')

for index, row in df.iterrows():
    work_composer = row['Composer']
    work_title = row['Mass']
    movement_title = row['Movement']
    source = row['Source']
    sib_file = row['Sibelius file']
    pdf_file = row['pdf file']
    xml_file = row['xml file']
    midi_file = row['midi file']

    sibelius = pt.SymbolicEncoder.create(software_name='Sibelius', software_version='Dunno')
    xml_maker = pt.SymbolicEncoder.create(software_name='XML Maker', software_version='Dunno')
    midi_maker = pt.SymbolicEncoder.create(software_name='MIDI Maker', software_version='Dunno')
    pdf_maker = pt.ImageEncoder.create(software_name='PDF Maker', software_version='Dunno')

    if str(work_composer) != 'nan' and str(work_title) != 'nan':
        # Adding Musical work
        work, was_created = pt.MusicalWork.get_or_create(title=work_title, composer=work_composer, genre='Mass')
        work_instance, was_created = pt.MusicalInstance.get_or_create(title=work_title)
        pt.InstanceOfWork.get_or_create(work=work, instance=work_instance)

        # Adding Section
        created = pt.Section.create(title=movement_title)
        work_and_movement_title = work_title + " : " + movement_title
        movement_instance = pt.MusicalInstance.create(title=work_and_movement_title)
        pt.InstanceOfSection.get_or_create(instance=movement_instance, section=created)
        pt.SectionInWork.create(section=created, work=work)

        # Adding Source
        source_of_work, was_created = pt.MusicalSource.get_or_create(title=source,
                                                                     musical_instance=work_instance)
        source_of_movement = pt.MusicalSource.create(title=source,
                                                     musical_instance=movement_instance)

        # Adding Sibelius file
        if str(sib_file) != 'nan':
            file_name = work_and_movement_title + ' Sibelius'
            file_type = '.sib'
            file_size = 123456
            version = '1.2'
            file = sib_file
            pt.SymbolicMusic.create(file_name=file_name, file_type=file_type, file_size=file_size,
                                    version=version, file=file, encoder=sibelius,
                                    musical_instance=movement_instance)

        # Adding XML file
        if str(xml_file) != 'nan':
            file_name = work_and_movement_title + ' XML'
            file_type = '.xml'
            file_size = 56586
            version = '3.4'
            file = sib_file
            pt.SymbolicMusic.create(file_name=file_name, file_type=file_type, file_size=file_size,
                                    version=version, file=file, encoder=xml_maker,
                                    musical_instance=movement_instance)

        # Adding MIDI file
        if str(xml_file) != 'nan':
            file_name = work_and_movement_title + ' MIDI'
            file_type = '.mid'
            file_size = 356457
            version = '5.6'
            file = sib_file
            pt.SymbolicMusic.create(file_name=file_name, file_type=file_type, file_size=file_size,
                                    version=version, file=file, encoder=midi_maker,
                                    musical_instance=movement_instance)

        # Adding PDF file
        if str(pdf_file) != 'nan':
            file_name = work_and_movement_title + ' PDF'
            file_type = '.pdf'
            file_size = 234236
            version = '1.4'
            file = sib_file
            pt.SymbolicMusic.create(file_name=file_name, file_type=file_type, file_size=file_size,
                                    version=version, file=file, encoder=pdf_maker,
                                    musical_instance=movement_instance)
