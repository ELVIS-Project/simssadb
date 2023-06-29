from dal import autocomplete
from django.db.models import Q
from database.models import GenreAsInStyle, GenreAsInType, GeographicArea, \
    Instrument, Software, Archive, File, MusicalWork, Person


class StyleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = GenreAsInStyle.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        return True

class FileAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = File.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        return True

class TypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = GenreAsInType.objects.all().order_by("name")

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


class SoftwareAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Software.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        return True


class ArchiveAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Archive.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        return True


class MusicalWorkAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = MusicalWork.objects.all()

        if self.q:
            qs = qs.filter(Q(contributors__given_name__icontains=self.q) 
                           | Q(contributors__surname__icontains=self.q)
                           | Q(variant_titles__icontains=self.q))

        return qs

    def has_add_permission(self, request):
        return True
    
    def get_results(self, context):
        results = []

        for musical_work in context["object_list"]:
            result = {
                "id": str(musical_work.pk),
                "text": musical_work.variant_titles[0],  # First element of variant_titles
                "selected_text": musical_work.variant_titles[0],  # First element of variant_titles
            }

            if musical_work.contributors.exists():
                first_contributor = musical_work.contributors.first()
                result["text"] += " - " + str(first_contributor)  # Append first contributor
                result["selected_text"] += " - " + str(first_contributor)  # Append first contributor

            results.append(result)

        return results
    
class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Person.objects.all()

        if self.q:
            qs = qs.filter(Q(given_name__icontains=self.q) 
                           | Q(surname__icontains=self.q))

        return qs

    def has_add_permission(self, request):
        return True
