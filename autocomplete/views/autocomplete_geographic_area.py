from dal import autocomplete
from autocomplete.models import AutocompleteGeographicArea


class AutocompleteGeographicAreaView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = AutocompleteGeographicArea.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        return True
