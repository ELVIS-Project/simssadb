import os
import sys

proj_path = "../../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")
sys.path.append(os.getcwd())

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.genre_as_in_type import GenreAsInType


def parseGenre(name_input):
    try:
        return GenreAsInType.objects.get(name=name_input)
    except GenreAsInType.DoesNotExist:
        return None


print('Adding genres...')

file = open(os.getcwd() + '/sample_data/madrigal/genre.txt', 'r')

line = file.readline().rstrip('\n')

while line:
    g = parseGenre(line)

    if g is None:
        g = GenreAsInType(name=line)
        g.save()

    line = file.readline().rstrip('\n')

r = GenreAsInStyle(name='Renaissance')
r.save()
