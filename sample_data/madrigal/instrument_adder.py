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

from database.models.instrument import Instrument


def parseInstrument(name_input):
    try:
        return Instrument.objects.get(name=name_input)
    except Instrument.DoesNotExist:
        return None


print('Adding instruments...')

file = open(os.getcwd() + '/sample_data/madrigal/instrument.txt', 'r')

line = file.readline().rstrip('\n')

while line:
    i = parseInstrument(line)

    if i is None:
        i = Instrument(name=line)
        i.save()

    line = file.readline().rstrip('\n')
