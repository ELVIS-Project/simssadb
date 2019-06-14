from django.contrib.postgres.aggregates.general import StringAgg
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import CharField, Count, F, Value, Q, Case, When
from django.views.generic import ListView
from database.models import (
    GenreAsInStyle,
    GenreAsInType,
    MusicalWork,
    Person,
    Section,
    Instrument,
    SymbolicMusicFile,
)


class SearchForm(forms.Form):
    def __init__(self, facet_groups=None, *args, **filters):
        super(SearchForm, self).__init__(*args, **filters)
        if facet_groups:
            for facet_key, facet_values in facet_groups.items():
                choices = []
                for value in facet_values:
                    text = value["facet_name"]
                    count = value["facet_count"]

                    choices.append((text, "{0}({1})".format(text, count)))

                self.fields[facet_key].choices = choices

    widget = forms.CheckboxSelectMultiple(
        attrs={"class": "pre-scrollable", "style": "overflow:auto"}
    )
    query = forms.CharField(required=False, label="Search ")
    types = forms.MultipleChoiceField(
        widget=widget, required=False, label="Genre (type of work)"
    )
    styles = forms.MultipleChoiceField(
        widget=widget, required=False, label="Genre (sytle)"
    )
    composers = forms.MultipleChoiceField(
        widget=widget, required=False, label="Composers"
    )
    instruments = forms.MultipleChoiceField(
        widget=widget, required=False, label="Instruments"
    )
    file_formats = forms.MultipleChoiceField(
        widget=widget, required=False, label="Symbolic Music File Formats"
    )


class PostgresSearchView(ListView):
    model = MusicalWork
    context_object_name = "works"
    template_name = "search/pg_search.html"
    queryset = MusicalWork.objects.none()
    form = SearchForm()

    def get_queryset(self):
        if len(self.request.GET):
            query = SearchQuery(self.request.GET["query"])
            rank_annotation = SearchRank(F("search_document"), query)
            self.queryset = (
                MusicalWork.objects.annotate(rank=rank_annotation)
                .filter(search_document=query)
                .order_by("-rank")
                .prefetch_related(
                    "genres_as_in_type",
                    "genres_as_in_style",
                    "contributions",
                    "contributions__person",
                    "sections",
                    "sections__parts__written_for",
                    "source_instantiations__manifested_by_sym_files",
                )
            )
            query_string = self.request.GET.getlist("query")
            facets = {
                "types": {
                    "selected": self.request.GET.getlist("types"),
                    "lookup": "genres_as_in_type__name",
                },
                "styles": {
                    "selected": self.request.GET.getlist("styles"),
                    "lookup": "genres_as_in_style__name",
                },
                "composers": {
                    "selected": self.request.GET.getlist("composers"),
                    "lookup": "contributions__person__surname",
                },
                "instruments": {
                    "selected": self.request.GET.getlist("instruments"),
                    "lookup": "sections__parts__instrument__name",
                },
                "formats": {
                    "selected": self.request.GET.getlist("file_formats"),
                    "lookup": "source_instantiations__manifested_by_sym_files__file_type",
                },
            }
            filters = {}  # Dict to hold our (facet : value) pairs
            for facet, data in facets.items():
                value = data["selected"]
                if value:
                    key = data["lookup"] + "__in"  # Add __in to filter the queryset
                    key_value_pair = {key: value}
                    filters.update(key_value_pair)
            self.queryset = self.queryset.filter(**filters)
            facet_groups = {}
            facet_groups["types"] = self.make_type_facets()
            facet_groups["styles"] = self.make_style_facets()
            facet_groups["composers"] = self.make_composer_facets()
            facet_groups["instruments"] = self.make_instrument_facets()
            facet_groups["file_formats"] = self.make_file_format_facets()
            # facet_groups["sacred"] = self.make_sacred_or_secular_facets()
            # facet_groups["certainty"] = self.make_certainty_facets()
            self.form = SearchForm(facet_groups=facet_groups, data=self.request.GET)
        return self.queryset

    def get_context_data(self, *args, **filters):
        context = super().get_context_data(**filters)
        context["form"] = self.form
        return context

    def make_type_facets(self):
        ids = list(self.get_queryset().values_list("id", flat=True))
        type_facets = (
            GenreAsInType.objects.filter(musical_works__in=ids).annotate(
                count=Count("musical_works")
            )
        ).values_list("name", "count")
        return type_facets

    def make_style_facets(self):
        ids = list(self.get_queryset().values_list("id", flat=True))
        style_facets = (
            GenreAsInStyle.objects.filter(musical_works__in=ids).annotate(
                count=Count("musical_works")
            )
        ).values_list("name", "count")
        return style_facets

    def make_composer_facets(self):
        ids = list(self.get_queryset().values_list("id", flat=True))
        composer_facets = (
            Person.objects.filter(contributions__contributed_to_work__in=ids).annotate(
                count=Count("contributions__contributed_to_work")
            )
        ).values_list("surname", "count")
        return composer_facets

    def make_instrument_facets(self):
        ids = list(self.get_queryset().values_list("id", flat=True))
        instrument_facets = (
            Instrument.objects.filter(parts__section__musical_work__in=ids).annotate(
                count=Count("parts__section__musical_work")
            )
        ).values_list("name", "count")
        return instrument_facets

    def make_file_format_facets(self):
        ids = list(self.get_queryset().values_list("id", flat=True))
        file_format_facets = (
            SymbolicMusicFile.objects.filter(
                Q(manifests__sections__musical_work__in=ids)
                | Q(manifests__work__in=ids)
            )
            .values("file_type")
            .annotate(count=Count("file_type"))
        ).values_list("file_type", "count")
        return file_format_facets

    def make_sacred_or_secular_facets(self):
        sacred_or_secular_facets = self.get_queryset().aggregate(
            true_count=Count(Case(When(_sacred_or_secular=True, then=Value(1)))),
            false_count=Count(Case(When(_sacred_or_secular=False, then=Value(1)))),
            none_count=Count(Case(When(_sacred_or_secular=None, then=Value(1)))),
        )
        return sacred_or_secular_facets

    def make_certainty_facets(self):
        query_set = self.get_queryset().prefetch_related("contributions")
        trues = len(
            [work for work in query_set.iterator() if work.certainty_of_attributions]
        )
        falses = len(
            [
                work
                for work in query_set.iterator()
                if not work.certainty_of_attributions
            ]
        )
        return {"certain": trues, "uncertain": falses}
