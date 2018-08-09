from django.http import JsonResponse, HttpResponse
from api.viaf import ViafAPI
from SPARQLWrapper import SPARQLWrapper, JSON
from django.shortcuts import redirect, render
from django.contrib import messages
import json


def GetVIAFResult(request):
    """
    A function that gets VIAF result from the input text
    :param request:
    :return:
    """
    if request.method == "GET" and 'q' in request.GET:
        value = request.GET['q']
        """Return JSON with suggested VIAF ids and display names."""
        viaf = ViafAPI()
        result = viaf.suggest(value)
    return result, viaf


def ViafComposerSearch(request):
    result, viaf = GetVIAFResult(request)
        # check for empty search result and return empty json response
    if result is None:
        return JsonResponse({'results': []})

    result = [item for item in result
       if item['nametype'] == 'personal']

    return JsonResponse({
        'results': [dict(
            uri=viaf.uri_from_id(item['viafid']),
            id=item['viafid'],
            text=item['displayForm'],
        ) for item in result]
    })


def ViafComposerSearchAutoComplete(request):
    """
    This function get the result from VIAF auto-complete module and parse the results
    :param request:
    :return:
    """
    if request.method == "GET" and 'q' in request.GET:
        result_string = request.GET['q']
    metadata = [result_string.strip(',') for result_string in result_string.split(' ')]
    viaf = ViafAPI()
    uri = viaf.uri_from_id(metadata[0])
    messages.error(request, uri, extra_tags='authority_control_url')
    has_date = 0  # whether the result strings contains date or not
    for i, item in enumerate(metadata):
        if item.find('-') != -1 and any(char.isdigit() for char in item):  # date must have - with digits
            date = item.split('-')
            messages.error(request, date[0].strip('('), extra_tags='range_date_birth')  # sometimes the dates are wrapped with ()
            messages.error(request, date[1].strip(')'), extra_tags='range_date_death')
            has_date = 1
            break
    # the 2 lines of code below will refresh messages
    storage = messages.get_messages(request)
    storage.used = True

    messages.error(request, metadata[1], extra_tags='surname')
    if len(metadata) > 1:
        if has_date:
            messages.error(request, ' '.join(map(str, metadata[2:i])), extra_tags='given_name') # consider the first
            # is the last name, and all the stuff between the last name and date is given name
        else:
            messages.error(request, ' '.join(map(str, metadata[2:i + 1])), extra_tags='given_name')
    return redirect('person')


def WikidataQuery(query):
    """
    Pass query and return results
    :param sparql:
    :return:
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return result

def GetWikidataComposerResult(request):
    """
    Get the dict of composer results from Wikidata
    :param request:
    :return:
    """
    if request.method == "GET" and 'q' in request.GET:
        value = request.GET['q']
        result = WikidataQuery("""
                SELECT ?item ?label ?date_of_birth ?date_of_death ?place_of_birth ?place_of_birthLabel ?place_of_death ?place_of_deathLabel ?given_name ?given_nameLabel ?family_name ?family_nameLabel WHERE {
                ?item wdt:P106 wd:Q36834.
                SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                ?item rdfs:label ?label.
                FILTER((LANG(?label)) = "en")
                FILTER(CONTAINS(lcase(str(?label)), "%s"))
                OPTIONAL { ?item wdt:P569 ?date_of_birth. }
                OPTIONAL { ?item wdt:P570 ?date_of_death. }
                OPTIONAL { ?item wdt:P19 ?place_of_birth. }
                OPTIONAL { ?item wdt:P20 ?place_of_death. }
                OPTIONAL { ?item wdt:P735 ?given_name. }
                OPTIONAL { ?item wdt:P734 ?family_name. }
                }
            """ % (value.lower()))
        return result


def wikidata_fix_name(item):
    """
    Fix missing given name and last name part from wikidata
    :return:
    """
    name_list = item['label']['value'].split(' ')
    if 'family_nameLabel' in item:
        if 'given_nameLabel' in item:
            if item['family_nameLabel']['value'] in name_list:
                last_name_ptr = name_list.index(item['family_nameLabel']['value'])
                item['given_nameLabel']['value'] = " ".join(name_list[
                                                            :last_name_ptr])  # Except for the last name, the content before it should all be given name
                if last_name_ptr + 1 <= len(name_list) - 1:  # we append things after the last name, like 'I'
                    item['family_nameLabel']['value'] += " " + " ".join(name_list[last_name_ptr + 1:])
    return item

def WikidataComposerSearchAutoFill(request):
    """
    Automatically fill person form using Wikidata results
    :param request:
    :return:
    """
    result = GetWikidataComposerResult(request)
    for item in result["results"]["bindings"]:
        item = wikidata_fix_name(item)
    return render(request, 'database/auto-fill-result.html', {'parameters': result["results"]["bindings"]})


def FillForm(request):
    """
    Parse the result from JSON and pass it to the form page
    :param request:
    :return:
    """
    if request.method == "GET" and 'q' in request.GET:
        value = request.GET['q']
    result = json.loads(value)
    storage = messages.get_messages(request)
    storage.used = True
    for key in result:
        messages.error(request,result[key] , extra_tags=key)
    return redirect('person')

def WikidataComposerSearch(request):

    result = GetWikidataComposerResult(request)
    # check for empty search result and return empty json response
    if result is None:
        return JsonResponse({'results': []})

    return JsonResponse({
        'results': [dict(
            uri=item["item"]["value"],
            name=item["label"]["value"],
            # range_date_birth=item["date_of_birth"]["value"],
            # range_date_death=item["date_of_death"]["value"],
            # birth_location=item["place_of_birthLabel"]["value"],
            # death_location=item["place_of_deathLabel"]["value"],
            # the lines above throws error is because some of the fields do not exist for every result
        ) for item in result["results"]["bindings"]]
    })