from django.conf.urls import url

from api.views import ViafComposerSearch, WikidataComposerSearch, ViafComposerSearchAutoFill

urlpatterns = [
    url(r'^search/wikidata/$', WikidataComposerSearch, name='wikidata-search'),
    url(r'^search/viaf/$', ViafComposerSearch, name='viaf-search'),
    url(r'^search/viaf/auto-fill/$', ViafComposerSearchAutoFill, name='viaf-search-auto-fill'),
]
