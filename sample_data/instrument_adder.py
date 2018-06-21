import os, sys

proj_path = "/Users/gustavo/Development/simssadb"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from database.models.instrument import Instrument

file = open('/Users/gustavo/Development/simssadb/sample_data/medprf.csv', 'r')

line = file.readline().rstrip('\n')

while line:
    i = Instrument(name=line)
    i.save()
    line = file.readline().rstrip('\n')

instruments = Instrument.objects.all()

for i in instruments:
    print(i.id, i.name)
