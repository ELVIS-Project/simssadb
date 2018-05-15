from prototype_sql import *


# Get all masses
query = MusicalWork.select()
works = [(work.title, work.composer) for work in query]
print(works)

print('+++' * 20)

# Get all instances
query = MusicalInstance.select()
instances = [instance.title for instance in query]
print(instances)

print('+++' * 20)

# Relationship between instances and works
query = InstanceOfWork.select()
pairs = [(instanceOf.work.title, instanceOf.instance.title) for instanceOf in query]
for pair in pairs:
    if pair[0] != pair[1]:
        print('Error!')

print('+++' * 20)

# Relationship between instances and sections
query = InstanceOfSection.select()
pairs = [(instanceOf.section.title, instanceOf.instance.title) for instanceOf in query]
for pair in pairs:
    print(pair[0] + " --> " + pair[1])

print('+++' * 20)

# Relationship between works and sections
query = SectionInWork.select()
pairs = [(inWork.work.title, inWork.work.composer, inWork.section.title) for inWork in query]
for pair in pairs:
    print(pair[1] + " " + pair[0] + " --> " + pair[2])

print('+++' * 20)

# Get all symbolic files
query = SymbolicMusic.select()
files = [(file.file_name, file.file) for file in query]
print(files)

print('+++' * 20)
print('\n')

# More advanced queries

# Get me the movements of all the pieces written by P. de la Rue which
# have both a XML file and an image
big_query = (MusicalWork.select()
             .join(SectionInWork)
             .join(InstanceOfSection, on=(InstanceOfSection.section == SectionInWork.section))
             .join(SymbolicMusic, on=(SymbolicMusic.musical_instance == InstanceOfSection.instance))
             .join(Image, on=(Image.musical_instance == InstanceOfSection.instance))
             .switch(InstanceOfSection).join(Section)
             .where((SymbolicMusic.file_type == '.xml') & (MusicalWork.composer == 'P. de la Rue'))
             .select(MusicalWork.composer, MusicalWork.title, Section.title.alias('sec_title'),
                     SymbolicMusic.file_name.alias('sym_file'), Image.file_name.alias('im_file')))

for record in big_query.dicts():
    print(record)

print('+++' * 20)
print('\n')

# Name and composer and ID of all the works that have both a Pleni and a Crucifixus

