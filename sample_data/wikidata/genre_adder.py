import os, sys
from api.autofill import autofill_genre
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
from sample_data.wikidata.location_adder import get_or_create


if __name__ == '__main__':
    print('Adding genres...')

    result = autofill_genre()
    Genre.objects.all().delete()
    for i, item in enumerate(result['results']['bindings']):
        if any(char.isdigit() for char in item['music_genreLabel']['value']): continue
        g, created = get_or_create(Genre, item['music_genreLabel']['value'])
        if created:
            g.save()
            print('genre added:', item['music_genreLabel']['value'])

    # file = open(os.getcwd() + '/sample_data/elvisdb/genre.txt', 'r')
    #
    # line = file.readline().rstrip('\n')
    #
    # while line:
    #     g = Genre(name=line)
    #     g.save()
    #     line = file.readline().rstrip('\n')
    #
    # genres = Genre.objects.all()
