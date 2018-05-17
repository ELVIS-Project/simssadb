from prototype_graph import *
import pandas as pd

df = pd.read_csv('/Users/gustavo/Development/SIMSSA-database/test-data/Josquin + La Rue Mass duos '
                 'Inventory - Sheet1.csv')
josquin = Composer(name='Josquin Des Pres').save()
rue = Composer(name='P. de la Rue').save()
mass = Genre(name='Mass').save()
jrp = MusicalSource(title='JRP').save()
opera = MusicalSource(title='Opera Omnia 1989').save()
sibelius = SymbolicEncoder(software_name='Sibelius', software_version='Dunno').save()
xml_maker = SymbolicEncoder(software_name='XML Maker', software_version='Dunno').save()
midi_maker = SymbolicEncoder(software_name='MIDI Maker', software_version='Dunno').save()
pdf_maker = ImageEncoder(software_name='PDF Maker', software_version='Dunno').save()

for index, row in df.iterrows():
    work_composer = row['Composer']
    work_title = row['Mass']
    movement_title = row['Movement']
    source = row['Source']
    sib_file = row['Sibelius file']
    pdf_file = row['pdf file']
    xml_file = row['xml file']
    midi_file = row['midi file']

    if str(work_composer) != 'nan' and str(work_title) != 'nan':
        # Adding Musical work
        try:
            work = MusicalWork.nodes.get(title=work_title)
            print('Did not create a new work')
        except:
            print('Creating a new work')
            print("Title: " + work_title + " Composer: " + work_composer)
            work = MusicalWork(title=work_title).save()
            work.genre.connect(mass)
            instance_of_work = MusicalInstance(title=work_title).save()
            instance_of_work.instantiates_work.connect(work)
            MusicalSource.nodes.get(title=source).source_of.connect(instance_of_work)
        try:
            Composer.nodes.get(name=work_composer).composed_work.connect(work)
        except:
            print("Composer not found")

        # Adding section
        section = Section(title=movement_title).save()
        section.part_of.connect(work)
        work_and_movement_title = work_title + " : " + movement_title
        instance_of_section = MusicalInstance(title=work_and_movement_title).save()
        instance_of_section.instantiates_section.connect(section)
        MusicalSource.nodes.get_or_none(title=source).source_of.connect(instance_of_section)

        # Adding sibelius file
        if str(sib_file) != 'nan':
            file_name = work_and_movement_title + ' Sibelius'
            file_type = '.sib'
            file_size = 123456
            version = '1.2'
            file = xml_file

            file = SymbolicMusic(file_name=file_name, file_size=file_size,
                                 file_type=file_type, version=version, file=file).save()
            file.manifests.connect(instance_of_section)
            file.encoded_with.connect(sibelius)

        # Adding xml file
        if str(xml_file) != 'nan':
            file_name = work_and_movement_title + ' XML'
            file_type = '.xml'
            file_size = 56586
            version = '3.4'
            file = xml_file

            file = SymbolicMusic(file_name=file_name, file_size=file_size,
                                 file_type=file_type, version=version, file=file).save()
            file.manifests.connect(instance_of_section)
            file.encoded_with.connect(xml_maker)

        # Adding MIDI file
        if str(xml_file) != 'nan':
            file_name = work_and_movement_title + ' MIDI'
            file_type = '.mid'
            file_size = 356457
            version = '5.6'
            file = midi_file

            file = SymbolicMusic(file_name=file_name, file_size=file_size,
                                 file_type=file_type, version=version, file=file).save()
            file.manifests.connect(instance_of_section)
            file.encoded_with.connect(midi_maker)

        # Adding PDF file
        if str(pdf_file) != 'nan':
            file_name = work_and_movement_title + ' PDF'
            file_type = '.pdf'
            file_size = 234236
            version = '1.4'
            file = pdf_file

            file = Image(file_name=file_name, file_size=file_size,
                         file_type=file_type, version=version, file=file).save()
            file.manifests.connect(instance_of_section)
            file.encoded_with.connect(pdf_maker)

print('Done!')
