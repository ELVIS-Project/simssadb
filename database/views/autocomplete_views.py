from dal import autocomplete

from database.models import Instrument, GenreAsInStyle, GenreAsInType


class InstrumentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Instrument.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class TypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = GenreAsInType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class StyleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = GenreAsInStyle.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
