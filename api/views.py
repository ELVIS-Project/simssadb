from django.http import JsonResponse, HttpResponse
from api.viaf import ViafAPI
from SPARQLWrapper import SPARQLWrapper, JSON
from django.shortcuts import redirect
from django.contrib import messages


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


def ViafComposerSearchAutoFill(request):
    """
    A function that parses the result of
    :param request:
    :return:
    """
    result = GetVIAFResult(request)
    result_string = result[0][0]['displayForm']
    metadata = [result_string.strip() for result_string in result_string.split(',')]
    date = metadata[-1].split('-')
    # the 2 lines of code below will refresh messages
    storage = messages.get_messages(request)
    storage.used = True
    # Pass the context info into messages
    messages.error(request, metadata[0], extra_tags='surname')
    messages.error(request, metadata[1], extra_tags='given_name')
    messages.error(request, date[0], extra_tags='birth_date')
    messages.error(request, date[1], extra_tags='death_date')
    return redirect('person')


def WikidataComposerSearch(request):

    if request.method == "GET" and 'q' in request.GET:
        value = request.GET['q']
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery("""
            SELECT ?item ?label ?date_of_birth ?date_of_death WHERE {
            ?item wdt:P106 wd:Q36834.
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            ?item rdfs:label ?label.
            FILTER((LANG(?label)) = "en")
            FILTER(CONTAINS(lcase(str(?label)), "%s"))
            OPTIONAL { ?item wdt:P569 ?date_of_birth. }
            OPTIONAL { ?item wdt:P570 ?date_of_death. }
            }
        """ % (value.lower()))

        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        # check for empty search result and return empty json response
        if result is None:
            return JsonResponse({'results': []})

        return JsonResponse({
            'results': [dict(
                uri=item["item"]["value"],
                text=item["label"]["value"],
                # birth=item["date_of_birth"]["value"],
                # death=item["date_of_death"]["value"],
            ) for item in result["results"]["bindings"]]
        })