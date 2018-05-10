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


