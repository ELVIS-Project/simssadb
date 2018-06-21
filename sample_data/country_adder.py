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

from database.models.geographic_area import GeographicArea

file = open('/Users/gustavo/Development/simssadb/sample_data/countries.txt',
            'r')

line = file.readline().rstrip('\n')

while line:
    g = GeographicArea(name=line)
    g.save()
    line = file.readline().rstrip('\n')

genres = GeographicArea.objects.all()

for g in genres:
    print(g.id, g.name)
