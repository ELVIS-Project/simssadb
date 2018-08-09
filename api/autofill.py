from django.http import JsonResponse, HttpResponse
from api.viaf import ViafAPI
from SPARQLWrapper import SPARQLWrapper, JSON
from django.shortcuts import redirect, render
from django.contrib import messages
import json
from api.views import WikidataComposerQuery
def autofill_composer():
    result = WikidataComposerQuery(
                                   """
                                                   SELECT ?item ?label ?date_of_birth ?date_of_death ?place_of_birth ?place_of_birthLabel ?place_of_death ?place_of_deathLabel ?given_name ?given_nameLabel ?family_name ?family_nameLabel WHERE {
                                                   ?item wdt:P106 wd:Q36834.
                                                   SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                                                   ?item rdfs:label ?label.
                                                   FILTER((LANG(?label)) = "en")
                                                   OPTIONAL { ?item wdt:P569 ?date_of_birth. }
                                                   OPTIONAL { ?item wdt:P570 ?date_of_death. }
                                                   OPTIONAL { ?item wdt:P19 ?place_of_birth. }
                                                   OPTIONAL { ?item wdt:P20 ?place_of_death. }
                                                   ?item wdt:P735 ?given_name. 
                                                   ?item wdt:P734 ?family_name.
                                                   FILTER((YEAR(?date_of_birth)) < 1900)
                                                   }
                                               """

                                   )
    return result

