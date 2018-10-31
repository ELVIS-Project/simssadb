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

from database.models.software import Software

def parseSoftware(name_input, version_input):
    try:
        return Software.objects.get(name=name_input, version=version_input)
    except Software.DoesNotExist:
        return None


print('Adding software...')

with open(os.getcwd() + '/sample_data/madrigal/software.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        name_input = row[0]
        version_input = row[1]

        s = parseSoftware(name_input, version_input)

        if s is None:
            s = Software(name=name_input, version=version_input)
            s.save()
