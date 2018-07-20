import os, sys, csv

proj_path = "../../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from database.models.collection_of_sources import CollectionOfSources

def parseCollection(title_input):
    try:
        return CollectionOfSources.objects.get(title=title_input)
    except CollectionOfSources.DoesNotExist:
        return None

print('Adding collections...')

with open(os.getcwd() + '/sample_data/madrigal/collection.csv')\
    as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	title_input = row[0]
    	editorial_notes_input = row[1]
    	publication_date_start_input = row[2]
    	publication_date_end_input = row[3]

    	c = parseCollection(title_input)

    	if c is None:
	        c = CollectionOfSources(title=title_input)

	        if editorial_notes_input:
	            c.editorial_notes = editorial_notes_input

	        if publication_date_start_input and publication_date_end_input:
	            c.publication_date = (publication_date_start_input, publication_date_end_input)

	        c.save()