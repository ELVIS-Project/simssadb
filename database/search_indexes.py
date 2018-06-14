import datetime
from haystack import indexes
from database.models.geographic_area import GeographicArea
from database.models.person import Person
from database.models.institution import Institution
from database.models.instrument import Instrument
from database.models.genre import Genre


class InstrumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Instrument

