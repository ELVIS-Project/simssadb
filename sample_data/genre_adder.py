import os, sys

proj_path = "../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from database.models.genre import Genre

file = open(os.getcwd() + '/sample_data/elvisdb/genre.txt', 'r')

line = file.readline().rstrip('\n')

while line:
    g = Genre(name=line)
    g.save()
    line = file.readline().rstrip('\n')

genres = Genre.objects.all()

for g in genres:
    print(g.id, g.name)
