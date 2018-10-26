import csv
import os
import sys

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
from database.models.encoder import Encoder


def parseSoftware(name_input, version_input):
    try:
        return Software.objects.get(name=name_input, version=version_input)
    except Software.DoesNotExist:
        return None


def parseEncoder(software, work_flow_text_input):
    try:
        return Encoder.objects.get(software=software,
                                   work_flow_text=work_flow_text_input)
    except Encoder.DoesNotExist:
        return None


print('Adding encoders...')

with open(os.getcwd() + '/sample_data/madrigal/encoder.csv') \
        as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    for row in readCSV:
        name_input = row[0]
        version_input = row[1]
        work_flow_text_input = row[2]

        s = parseSoftware(name_input, version_input)

        if s is not None:
            e = parseEncoder(s, work_flow_text_input)

            if e is None:
                e = Encoder(work_flow_text=work_flow_text_input, software=s)
                e.save()
