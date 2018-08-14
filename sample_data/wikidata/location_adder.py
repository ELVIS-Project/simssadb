import os, sys
from api.autofill import autofill_location
proj_path = "../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from database.models.geographic_area import GeographicArea


def get_or_create(entity, name):
    """
    Used to create a place, which does not have a parent location
    :param entity:
    :param name:
    :return:
    """
    exist = entity.objects.filter(name=name).exists()
    if exist:
        instance = entity.objects.filter(name=name).first()
        return entity.objects.filter(name=name).first(), False
    else:
        instance = entity.objects.create(name=name)
        return instance, True


if __name__ == '__main__':

    print('Adding locations...')
    result = autofill_location()
    GeographicArea.objects.all().delete()
    for i, item in enumerate(result['results']['bindings']): # add cities later
        if 'cityLabel' in item and 'countryLabel' in item:
            if any(char.isdigit() for char in item['cityLabel']['value']): continue  # remove Q12345678 entries
            g = GeographicArea(name=item['cityLabel']['value'])
            country, created = get_or_create(GeographicArea, item['countryLabel']['value'])
            if created:
                print('country added:', item['countryLabel']['value'])
                country.save()
            print('city added:', item['cityLabel']['value'])
            g.part_of = country
            g.save()



