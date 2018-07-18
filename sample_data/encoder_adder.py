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

from database.models.software import Software
from database.models.encoder import Encoder

print('Adding encoders...')

with open(os.getcwd() + '/sample_data/elvisdb/encoder.csv')\
    as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    for row in readCSV:
    	software = Software.objects.get(name=row[0])
    	e = Encoder(work_flow_text=row[1], software=software)
    	e.save()