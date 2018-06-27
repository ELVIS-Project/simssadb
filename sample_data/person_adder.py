import os, sys, csv

proj_path = "../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from database.models.person import Person

with open(os.getcwd() + '/sample_data/composers.csv')\
        as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if row[1] and row[2]:
            p = Person(names=[row[0]], range_date_birth=(None, row[1]),
                       range_date_death=(None, row[2]))
        else:
            p = Person(names=[row[0]])
        p.save()

    people = Person.objects.all()
    for person in people:
        print(person.names, person.range_date_birth, person.range_date_death)


