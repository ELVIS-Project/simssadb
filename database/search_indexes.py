from haystack import indexes
from database.models.geographic_area import GeographicArea
from database.models.person import Person
from database.models.institution import Institution
from database.models.instrument import Instrument
from database.models.genre import Genre
from database.models.musical_work import MusicalWork
from database.models.section import Section


class InstrumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Instrument


class GenreIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Genre


class InstitutionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='website')

    def get_model(self):
        return Institution


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return Person


class GeographicAreaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return GeographicArea


class MusicalWorkIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    religiosity = indexes.BooleanField(model_attr='religiosity')

    def get_model(self):
        return MusicalWork


class SectionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Section
