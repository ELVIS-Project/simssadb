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

with open(os.getcwd() + '/sample_data/elvisdb/person.csv')\
    as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        p = Person(given_name=row[0])

        if row[1]:
            p.surname = row[1]

        if row[2]:
            p.range_date_birth = (None, row[2])

        if row[3]:
            p.range_date_death = (None, row[3])

        p.save()

    people = Person.objects.all()
    for person in people:
        print(person.given_name, person.surname, person.range_date_birth, person.range_date_death)


