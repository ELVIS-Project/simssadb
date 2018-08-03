from django.conf.urls import url

from api.views import ViafComposerSearch, WikidataComposerSearch,  ViafComposerSearchAutoComplete, WikidataComposerSearchAutoFill

urlpatterns = [
    url(r'^search/wikidata/$', WikidataComposerSearch, name='wikidata-search'),
    url(r'^search/viaf/$', ViafComposerSearch, name='viaf-search'),
    url(r'^search/viaf/auto-complete/$', ViafComposerSearchAutoComplete, name='viaf-search-auto-complete'),
    url(r'^search/wikidata/auto-fill/$', WikidataComposerSearchAutoFill, name='wikidata-composer-search-auto-fill'),
]
