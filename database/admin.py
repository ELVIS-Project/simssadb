from django.contrib import admin
from database.models.profile import Profile
from database.models.musical_work import MusicalWork
from database.models.section import Section
from database.models.part import Part
from database.models.genre import Genre
from database.models.geographic_area import GeographicArea
from database.models.instrument import Instrument
from database.models.symbolic_music_file import SymbolicMusicFile
from database.models.audio_file import AudioFile
from database.models.image_file import ImageFile
from database.models.research_corpus import ResearchCorpus
from database.models.experimental_study import ExperimentalStudy
from database.models.extracted_feature import ExtractedFeature
from database.models.source import Source
from database.models.person import Person
from database.models.institution import Institution
from database.models.archive import Archive
from database.models.collection_of_sources import CollectionOfSources
from database.models.contributed_to import ContributedTo
from database.models.encoder import Encoder
from database.models.software import Software
from database.models.validator import Validator

# Register your models here.

admin.site.register(Profile)
admin.site.register(MusicalWork)
admin.site.register(Section)
admin.site.register(Part)
admin.site.register(Genre)
admin.site.register(GeographicArea)
admin.site.register(Instrument)
admin.site.register(SymbolicMusicFile)
admin.site.register(AudioFile)
admin.site.register(ImageFile)
admin.site.register(ResearchCorpus)
admin.site.register(ExperimentalStudy)
admin.site.register(ExtractedFeature)
admin.site.register(Source)
admin.site.register(Person)
admin.site.register(Institution)
admin.site.register(Archive)
admin.site.register(CollectionOfSources)
admin.site.register(ContributedTo)
admin.site.register(Encoder)
admin.site.register(Software)
admin.site.register(Validator)
