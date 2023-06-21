import os
import sys
import csv
from datetime import date
import re
print('the original cwd at Locations folder', os.getcwd())
original_cwd = os.getcwd()
proj_path = "../../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)
print('the original cwd at Locations after specifying the proj path', os.getcwd())

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
from django.conf import settings

application = get_wsgi_application()

import requests
from bs4 import BeautifulSoup
from django.db import transaction

from database.models.geographic_area import GeographicArea


def scrape_geographic_areas():
    urls = [
        "https://id.loc.gov/vocabulary/geographicAreas.html",
        "https://id.loc.gov/vocabulary/countries.html",
    ]
    geographic_areas = []

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            area_elements = soup.select('li[rel="madsrdf:hasTopMemberOfMADSScheme skos:hasTopConcept"] a')
            for area_element in area_elements:
                area_name = area_element.text.strip()
                if "http" in area_name:
                    continue
                area_url = area_element["href"]
                geographic_areas.append((area_name, area_url))
        else:
            print("Error retrieving from " + str(url) + ": response status code was " + str(response.status_code))

    # Save geographic areas to the database
    with transaction.atomic():
        for area_name, area_url in geographic_areas:
            geographic_area = GeographicArea(name=area_name, authority_control_url=area_url)
            geographic_area.save()
            print(area_name, area_url)

if __name__ == "__main__":
    print("Adding standard geographic areas to the database...")
    scrape_geographic_areas()
