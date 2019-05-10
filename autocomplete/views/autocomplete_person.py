from dal import autocomplete
from autocomplete.models import AutocompletePerson
from django.db.models import Q


class AutocompletePerson(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = AutocompletePerson.objects.all()

        if self.q:
            qs = qs.filter(
                Q(given_name__istartswith=self.q) |
                Q(surname_istartswith=self.q))
        return qs

    def has_add_permission(self, request):
        return True
