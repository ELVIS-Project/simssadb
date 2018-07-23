import os, sys, csv

proj_path = "../../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from database.models.person import Person

def parsePerson(surname_input, given_name_input):
    if surname_input is not '':
        try:
            return Person.objects.get(surname=surname_input,
                given_name=given_name_input)
        except Person.DoesNotExist:
            return None
    else:
        try:
            return Person.objects.get(surname='', given_name=given_name_input)
        except Person.DoesNotExist:
            return None


print('Adding persons...')

with open(os.getcwd() + '/sample_data/madrigal/person.csv')\
    as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        given_name_input = row[0]
        surname_input = row[1]
        birth_input = row[2]
        death_input = row[3]
        viaf_url_input = row[4]
        viaf_key_input = row[5]

        p = parsePerson(surname_input, given_name_input)

        if p is None:
            p = Person(given_name=given_name_input)

            if surname_input:
                p.surname = surname_input

            if birth_input:
                p.range_date_birth = (None, birth_input)

            if death_input:
                p.range_date_death = (None, death_input)

            if viaf_url_input:
                p.authority_control_url = viaf_url_input

            if viaf_key_input:
                p.authority_control_key = viaf_key_input

            p.save()
