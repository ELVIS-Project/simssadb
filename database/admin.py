"""Register models in the Django admin site"""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from database.models.musical_work import MusicalWork
from database.models.section import Section
from database.models.part import Part
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.genre_as_in_type import GenreAsInType
from database.models.geographic_area import GeographicArea
from database.models.instrument import Instrument
from database.models.file import File
from database.models.research_corpus import ResearchCorpus
from database.models.experimental_study import ExperimentalStudy
from database.models.extracted_feature import ExtractedFeature
from database.models.source import Source
from database.models.person import Person
from database.models.archive import Archive
from database.models.contribution_musical_work import ContributionMusicalWork
from database.models.encoding_workflow import EncodingWorkFlow
from database.models.software import Software
from database.models.validation_workflow import ValidationWorkFlow
from database.models.feature_type import FeatureType
from database.models.source_instantiation import SourceInstantiation
from database.models.type_of_section import TypeOfSection

admin.site.register(MusicalWork, SimpleHistoryAdmin)
admin.site.register(Section, SimpleHistoryAdmin)
admin.site.register(Part, SimpleHistoryAdmin)
admin.site.register(GenreAsInStyle, SimpleHistoryAdmin)
admin.site.register(GenreAsInType, SimpleHistoryAdmin)
admin.site.register(GeographicArea, SimpleHistoryAdmin)
admin.site.register(Instrument, SimpleHistoryAdmin)
admin.site.register(File, SimpleHistoryAdmin)
admin.site.register(ResearchCorpus, SimpleHistoryAdmin)
admin.site.register(ExperimentalStudy, SimpleHistoryAdmin)
admin.site.register(ExtractedFeature, SimpleHistoryAdmin)
admin.site.register(Source, SimpleHistoryAdmin)
admin.site.register(Person, SimpleHistoryAdmin)
admin.site.register(Archive, SimpleHistoryAdmin)
admin.site.register(ContributionMusicalWork, SimpleHistoryAdmin)
admin.site.register(EncodingWorkFlow, SimpleHistoryAdmin)
admin.site.register(Software, SimpleHistoryAdmin)
admin.site.register(ValidationWorkFlow, SimpleHistoryAdmin)
admin.site.register(FeatureType, SimpleHistoryAdmin)
admin.site.register(SourceInstantiation, SimpleHistoryAdmin)
admin.site.register(TypeOfSection, SimpleHistoryAdmin)
