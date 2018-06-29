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

from database.models.collection_of_sources import CollectionOfSources

with open(os.getcwd() + '/sample_data/elvisdb/collection.csv')\
    as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row[0])
        c = CollectionOfSources(title=row[0])

        if row[1]:
            c.editorial_notes = row[1]

        c.save()

    # collections = CollectionOfSources.objects.all()
    # for collection in collections:
    #     print(collection.title)


