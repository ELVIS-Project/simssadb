from dal import autocomplete

from database.models import GenreAsInStyle, GenreAsInType, GeographicArea, Instrument


class StyleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = GenreAsInStyle.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        return True


class TypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = GenreAsInType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        return True


class GeographicAreaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = GeographicArea.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        return True


class InstrumentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Instrument.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        return True
