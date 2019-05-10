from dal import autocomplete
from autocomplete.models import AutocompleteInstrument


class AutocompleteInstrumentView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = AutocompleteInstrument.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        return True
