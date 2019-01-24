import os, sys, csv
from api.autofill import autofill_composer
from api.views import wikidata_fix_name
proj_path = "../../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from database.models.person import Person
from database.models.geographic_area import GeographicArea
from sample_data.wikidata.location_adder import get_or_create


def parsePerson(surname_input, given_name_input):
    if surname_input is not '':
        try:
            return Person.objects.get(surname=surname_input,
                given_name=given_name_input)
        except Person.DoesNotExist:
            return None
    else:
        try:
            return Person.objects.get(surname='', given_name=given_name_input)
        except Person.DoesNotExist:
            return None


if __name__ == '__main__':
    print('Adding persons...')

    result = autofill_composer()
    Person.objects.all().delete()

    for i, item in enumerate(result['results']['bindings']):
        if i > 0 and 'date_of_birth' in item and 'date_of_death' in item:
            if item['date_of_birth']['value'] == result['results']['bindings'][i-1]['date_of_birth']['value'] and item['date_of_death']['value'] == result['results']['bindings'][i-1]['date_of_death']['value']:
                continue # escape duplicated entries!
        item = wikidata_fix_name(item)
        if 'given_nameLabel' in item:
            given_name_input = item['given_nameLabel']['value']
        if 'family_nameLabel' in item:
            surname_input = item['family_nameLabel']['value']
        if 'date_of_birth' in item:
            birth_input = item['date_of_birth']['value'][:-10] # truncate T00:00:00Z part
        if 'date_of_death' in item and item['date_of_death']['value'][:-10] != 't':
            death_input = item['date_of_death']['value'][:-10]
        if 'place_of_birthLabel' in item:
            birth_location = item['place_of_birthLabel']['value']
        if 'place_of_deathLabel' in item:
            death_location = item['place_of_deathLabel']['value']
        viaf_url_input = item['item']['value']
        print('add person:', given_name_input , surname_input)
        p = parsePerson(surname_input, given_name_input)

        if p is None:
            p = Person(given_name=given_name_input)

            if surname_input:
                p.surname = surname_input

            if birth_input:
                p.range_date_birth = (None, birth_input)

            if death_input:
                p.range_date_death = (None, death_input)

            if viaf_url_input:
                p.authority_control_url = viaf_url_input
            if birth_location:
                location, created = get_or_create(GeographicArea, name=birth_location)
                p.birth_location = location

            if death_location:
                location, created = get_or_create(GeographicArea, name=death_location)
                p.death_location = location

            p.save()
