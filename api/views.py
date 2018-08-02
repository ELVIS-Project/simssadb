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

def ViafComposerSearchAutoComplete(request):
    """
    This function get the result from VIAF auto-complete module and parse the results
    :param request:
    :return:
    """
    if request.method == "GET" and 'q' in request.GET:
        result_string = request.GET['q']
    if result_string.find('-') == -1: return redirect('person')
    metadata = [result_string.strip(',') for result_string in result_string.split(' ')]
    for i, item in enumerate(metadata):
        if item.find('-') != -1 and any(char.isdigit() for char in item):  # date must have - with digits
            # for char in item:  # only keep digits
            #     if not char.isdigit():
            #         item = item.replace(char,'')
            date = item.split('-')
            break
    if date[0] == '' or date[1] == '': return redirect('person')  # only return person with both birth date and death date

    # the 2 lines of code below will refresh messages
    storage = messages.get_messages(request)
    storage.used = True
    viaf = ViafAPI()
    uri = viaf.uri_from_id(metadata[0])
    # Pass the context info into messages
    messages.error(request, metadata[1], extra_tags='surname')
    if len(metadata) > 1:
        messages.error(request, ' '.join(map(str, metadata[2:i])), extra_tags='given_name')  # consider
    messages.error(request, date[0] + '-01-01', extra_tags='range_date_birth')
    messages.error(request, date[1] + '-01-01', extra_tags='range_date_death')
    messages.error(request, uri, extra_tags='authority_control_url')
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