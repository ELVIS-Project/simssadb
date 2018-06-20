from django.conf.urls import url

from api.views import ViafComposerSearch, WikidataComposerSearch

urlpatterns = [
    url(r'^search/wikidata/$', WikidataComposerSearch, name='wikidata-search'),
    url(r'^search/viaf/$', ViafComposerSearch, name='viaf-search'),
]
