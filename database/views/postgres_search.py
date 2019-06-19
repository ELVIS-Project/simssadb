from collections import namedtuple
from typing import List

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Paginator
from django.db.models import Case, CharField, Count, F, Q, QuerySet, Value, When
from django.http import Http404
from django.views.generic import ListView

from database.forms.postgres_search_form import SearchForm
from database.models import (
    GenreAsInStyle,
    GenreAsInType,
    Instrument,
    MusicalWork,
    Person,
    Section,
    SymbolicMusicFile,
)


class Facet(object):
    def __init__(self, display_name, lookup, selected=[], facet_values=[]):
        self.display_name = display_name
        self.lookup = lookup
        self.selected = selected
        self.facet_values = facet_values


class FacetValue(object):
    def __init__(self, pk, display_name, count):
        self.pk = pk
        self.display_name = display_name
        self.count = count


class PostgresSearchView(ListView):
    model = MusicalWork
    context_object_name = "works"
    template_name = "search/pg_search.html"
    queryset = MusicalWork.objects.none()
    form = SearchForm()
    paginate_by = 10
    facets = {
        "types": Facet(
            display_name="Genre (Type of Work)", lookup="genres_as_in_type__pk"
        ),
        "styles": Facet(display_name="Genre (Style)", lookup="genres_as_in_style__pk"),
        "composers": Facet(display_name="Composer", lookup="contributions__person__pk"),
        "instruments": Facet(
            display_name="Instrument/Voice", lookup="sections__parts__written_for__pk"
        ),
        "file_formats": Facet(
            display_name="File Format",
            lookup="source_instantiations__manifested_by_sym_files__file_type",
        ),
        "sacred": Facet(display_name="Sacred or Secular", lookup="_sacred_or_secular"),
    }

    def get_queryset(self):
        q = self.request.GET.get("q")
        for key, facet in self.facets.items():
            selected = self.request.GET.getlist(key)
            if selected:
                facet.selected = selected
        return self.search(q=q, facets=self.facets)

    def search(self, q: str, facets) -> QuerySet:
        query = SearchQuery(q)
        rank_annotation = SearchRank(F("search_document"), query)
        queryset = (
            MusicalWork.objects.annotate(rank=rank_annotation)
            .filter(search_document=query)
            .order_by("-rank")
        )
        querys = Q()
        for key, facet in facets.items():
            querys &= self.make_facet_query(facet)
        return queryset.filter(querys)

    def make_facet_query(self, facet: Facet) -> Q:
        q_objects = Q()
        for selection in facet.selected:
            kwarg = {facet.lookup: selection}
            q_objects |= Q(**kwarg)
        return q_objects

    def get_context_data(self, *args):
        context = super().get_context_data()
        ids = list(self.get_queryset().values_list("id", flat=True))
        for key, facet in self.facets.items():
            if key == "types":
                facet.facet_values = self.make_type_facet_values(ids)
            elif key == "styles":
                facet.facet_values = self.make_style_facet_values(ids)
            elif key == "composers":
                facet.facet_values = self.make_composer_facet_values(ids)
            elif key == "instruments":
                facet.facet_values = self.make_instrument_facet_values(ids)
            elif key == "file_formats":
                facet.facet_values = self.make_file_format_facet_values(ids)
            elif key == "sacred":
                facet.facet_values = self.make_sacred_facet_values(ids)
        context["form"] = SearchForm(data=self.request.GET, facets=self.facets)
        return context

    def make_type_facet_values(self, ids):
        type_facet_values = []
        type_tuples = (
            GenreAsInType.objects.filter(musical_works__in=ids).annotate(
                count=Count("musical_works"), display_name=F("name")
            )
        ).values_list("pk", "display_name", "count")
        for type_tuple in type_tuples:
            type_facet_values.append(FacetValue(*type_tuple))
        return type_facet_values

    def make_style_facet_values(self, ids):
        style_facet_values = []
        style_tuples = (
            GenreAsInStyle.objects.filter(musical_works__in=ids).annotate(
                count=Count("musical_works"), display_name=F("name")
            )
        ).values_list("pk", "display_name", "count")
        for style_tuple in style_tuples:
            style_facet_values.append(FacetValue(*style_tuple))
        return style_facet_values

    def make_composer_facet_values(self, ids):
        composer_facet_values = []
        composer_tuples = (
            Person.objects.filter(
                contributions__contributed_to_work__in=ids,
                contributions__role="COMPOSER",
            ).annotate(count=Count("contributions__contributed_to_work"))
        ).values_list("pk", "given_name", "surname", "count")
        for composer_tuple in composer_tuples:
            facet_value = FacetValue(
                pk=composer_tuple[0],
                display_name="{0}, {1}".format(composer_tuple[2], composer_tuple[1]),
                count=composer_tuple[3],
            )
            composer_facet_values.append(facet_value)
        return composer_facet_values

    def make_instrument_facet_values(self, ids):
        instrument_facet_values = []
        instrument_tuples = (
            Instrument.objects.filter(parts__section__musical_work__in=ids).annotate(
                count=Count("parts__section__musical_work")
            )
        ).values_list("pk", "name", "count")
        for instrument_tuple in instrument_tuples:
            instrument_facet_values.append(FacetValue(*instrument_tuple))
        return instrument_facet_values

    def make_file_format_facet_values(self, ids):
        file_format_facet_values = []
        file_format_tuples = (
            SymbolicMusicFile.objects.filter(
                Q(manifests__sections__musical_work__in=ids)
                | Q(manifests__work__in=ids)
            )
            .values_list("file_type")
            .annotate(display_name=F("file_type"), count=Count("file_type"))
        )
        for file_format_tuple in file_format_tuples:
            file_format_facet_values.append(FacetValue(*file_format_tuple))
        return file_format_facet_values

    def make_sacred_facet_values(self, ids):
        aggregated_query = MusicalWork.objects.filter(id__in=ids).aggregate(
            trues=Count("_sacred_or_secular", filter=Q(_sacred_or_secular=True)),
            falses=Count("_sacred_or_secular", filter=Q(_sacred_or_secular=False)),
            nones=Count("_sacred_or_secular", filter=Q(_sacred_or_secular=None)),
        )
        if aggregated_query["trues"] > 0:
            trues = FacetValue(
                pk=True, display_name="Sacred", count=aggregated_query["trues"]
            )
        else:
            trues = None
        if aggregated_query["falses"] > 0:
            falses = FacetValue(
                pk=False, display_name="Secular", count=aggregated_query["falses"]
            )
        else:
            falses = None
        if aggregated_query["nones"] > 0:
            nones = FacetValue(
                pk=None, display_name="Non-Applicable", count=aggregated_query["nones"]
            )
        else:
            nones = None
        sacred_facet_values = [trues, falses, nones]
        sacred_facet_values = [i for i in sacred_facet_values if i is not None]
        return sacred_facet_values
