from api.views import WikidataQuery


def autofill_composer():
    result = WikidataQuery(
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


def autofill_location():
    result = WikidataQuery(
        """
                       SELECT ?city ?cityLabel ?country ?countryLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  ?city wdt:P31 wd:Q515.
  OPTIONAL { ?city wdt:P17 ?country. }
}
                    """

    )
    return result