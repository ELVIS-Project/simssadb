"""Parses an XML file containing RDF data from VIAF and adds the
Person entities found to the person_autcomplete table"""
import os
import re
import string
import sys
import xml.etree.ElementTree as ET
from dateutil.parser import parse

proj_path = "../"
os.chdir(proj_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")
sys.path.append(os.getcwd())

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from autocomplete.models import AutocompletePerson


def choose_latin_name(string_list):
    try:
        for string in string_list:
            if bool(re.search('(?=.*[a-z])', string)):
                string = string.replace(',', '')
                return string
        return None
    except:
        return None

file = '/Volumes/Share 0/VIAF-datasets/viaf-20190505-clusters-rdf.xml'

with open(file) as f:
    i = 0
    for line in f:
        if '<rdf:type rdf:resource="http://schema.org/Person"/>' in line:
            line = line[line.index('<'):]
            root = ET.fromstring(line)

            family_names = []
            given_names = []
            for name in root.iter("{http://schema.org/}familyName"):
                family_names.append(name.text)
            for name in root.iter("{http://schema.org/}givenName"):
                given_names.append(name.text)
            try:
                birth_date = next(
                    root.iter("{http://schema.org/}birthDate")).text
                birth_date = parse(birth_date).date
            except:
                birth_date = None
            try:
                death_date = next(
                    root.iter("{http://schema.org/}deathDate")).text
                death_date = parse(death_date).date
            except:
                death_date = None
            try:
                viaf_id = next(
                    root.iter("{http://purl.org/dc/terms/}identifier")).text
                viaf_id = int(viaf_id)
            except:
                viaf_id = None
            try:
                viaf_uri = next(root.iter("{http://xmlns.com/foaf/0.1/}focus")
                                ).attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
            except:
                viaf_uri = None
            if family_names:
                family_name = choose_latin_name(family_names)
            else:
                family_name = None
            if given_names:
                given_name = choose_latin_name(given_names)
            else:
                given_name = None

            if family_name or given_name:
                person = AutocompletePerson(given_name=given_name,
                                            surname=family_name)
                person.range_date_birth = (None, birth_date)
                person.range_date_death = (None, death_date)
                person.authority_control_key = viaf_id
                person.authority_control_url = viaf_uri
                print(person.given_name, person.surname, person.authority_control_key)
                person.save()

            if (i % 1000 == 0):
                progress = int((i/11000000) * 100)
                print(progress, "%")
