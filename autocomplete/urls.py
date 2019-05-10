from django.conf.urls import url
from autocomplete.views import (AutocompleteGeographicAreaView,
                                AutocompleteInstrumentView,
                                AutocompletePersonView,
                                AutocompleteStyleView, AutocompleteTypeView)

urlpatterns = [
    url(r'^autocomplete/geographicarea/$',
        AutocompleteGeographicAreaView.as_view(),
        name='autocomplete-geographicarea'),
    url(r'^autocomplete/instrument/$',
        AutocompleteInstrumentView.as_view(),
        name='autocomplete-instrument'),
    url(r'^autocomplete/person/$',
        AutocompletePersonView.as_view(),
        name='autocomplete-person'),
    url(r'^autocomplete/style/$',
        AutocompleteStyleView.as_view(),
        name='autocomplete-style'),
    url(r'^autocomplete/type/$',
        AutocompleteStyleView.as_view(),
        name='autocomplete-type')
]
