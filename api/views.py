from django.http import JsonResponse
from api.viaf import ViafAPI
from SPARQLWrapper import SPARQLWrapper, JSON

def ViafComposerSearch(request):

    if request.method == "GET" and 'q' in request.GET:
        value = request.GET['q']
        """Return JSON with suggested VIAF ids and display names."""
        viaf = ViafAPI()

        result = viaf.suggest(value)

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