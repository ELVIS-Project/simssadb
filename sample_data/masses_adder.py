import csv
import os
import sys


proj_path = "../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from database.models.musical_work import MusicalWork
from database.models.contributed_to import ContributedTo
from database.models.person import Person
from database.models.genre import Genre
from database.models.software import Software
from database.models.encoder import Encoder

sw = Software(name='Sibelius')
sw.save()
encoder = Encoder(work_flow_text='I encoded this with Sibelius',
                  software=sw)
encoder.save()

with open(os.getcwd() + '/sample_data/masses.csv')\
        as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        mass_genre = Genre.objects.filter(name='mass')[0]
        renaissance_genre = Genre.objects.filter(name='renaissance')[0]
        pierre = Person.objects.get(names__contains=['La Rue, Pierre de'])
        josquin = Person.objects.get(names__contains='{Josquin Des Prez}')
        print(mass_genre)
        for row in readCSV:
            if row[0] == 'P. de la Rue':
                print('Composer is Pierre')
                w = MusicalWork(variant_titles=[row[1]])
                w.save()
                w.genres_as_in_type.add(mass_genre)
                w.genres_as_in_style.add(renaissance_genre)
                w.sacred_or_secular = True
                w.save()
                ctr = ContributedTo(person=pierre, certain=True,
                                    role='COMPOSER',
                                    contributed_to_work=w)
                ctr.save()
            if row[0] == 'Josquin Des Pres':
                print('Composer is Josquin')
                w = MusicalWork(variant_titles=[row[1]])
                w.save()
                w.genres_as_in_type.add(mass_genre)
                w.genres_as_in_style.add(renaissance_genre)
                w.sacred_or_secular = True
                w.save()
                ctr = ContributedTo(person=josquin, certain=True,
                                    role='COMPOSER',
                                    contributed_to_work=w)
                ctr.save()
            if row[0] == 'Josquin Des Pres (not secure)':
                print('Maybe Josquin???')
                w = MusicalWork(variant_titles=[row[1]])
                w.save()
                w.genres_as_in_type.add(mass_genre)
                w.genres_as_in_style.add(renaissance_genre)
                w.sacred_or_secular = True
                w.save()
                ctr = ContributedTo(person=josquin, certain=False,
                                    role='COMPOSER',
                                    contributed_to_work=w)
                ctr.save()
