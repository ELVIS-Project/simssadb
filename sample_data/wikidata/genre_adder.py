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

from database.models.genre_as_in_style import GenreAsInStyle
from sample_data.wikidata.location_adder import get_or_create


if __name__ == '__main__':
    print('Adding genres as in style...')
    result = autofill_genre()
    GenreAsInStyle.objects.all().delete()
    for i, item in enumerate(result['results']['bindings']):
        if any(char.isdigit() for char in item['music_genreLabel']['value']): continue
        g, created = get_or_create(GenreAsInStyle, item['music_genreLabel']['value'])
        if created:
            g.save()
            print('genre as in style added:', item['music_genreLabel']['value'])
    print('Adding genres as in type...')
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'genre_as_in_type.txt'), 'r')
    line = file.readline().rstrip('\n')
    for line in file.readlines():
        line = line.strip('\n')
        if line == '': continue
        g, created = get_or_create(GenreAsInStyle, line)
        if created:
            g.save()
            print('genre as in type added:', line)

