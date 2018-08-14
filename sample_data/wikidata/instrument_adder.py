import os, sys
from api.autofill import autofill_instrument
proj_path = "../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from database.models.instrument import Instrument
from sample_data.wikidata.location_adder import get_or_create


if __name__ == '__main__':
    print('Adding instruments...')

    result = autofill_instrument()
    Instrument.objects.all().delete()
    for i, item in enumerate(result['results']['bindings']):
        if any(char.isdigit() for char in item['musical_instrumentLabel']['value']): continue
        i, created = get_or_create(Instrument, item['musical_instrumentLabel']['value'])
        if created:
            i.save()
            print('instrument added:', item['musical_instrumentLabel']['value'])

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
