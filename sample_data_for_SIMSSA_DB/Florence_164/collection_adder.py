import csv
import os
import sys

proj_path = "../../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from database.models.source import Source


print('Adding collections...')

with open(os.getcwd() + '/sample_data_for_SIMSSA_DB/Florence_164/collection.csv') \
        as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        title_input = row[0]
        editorial_notes_input = row[1]
        publication_date_start_input = row[2]
        publication_date_end_input = row[3]
        url = row[4]
        source = Source.objects.get_or_create(
            title=title_input, source_type='DIGITAL', editorial_notes=editorial_notes_input, url=url,
            date_range_year_only=(
                    int(publication_date_start_input), int(publication_date_end_input))
        )[0]

        print(source, " added to the database")
