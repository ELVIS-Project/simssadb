from database.models.custom_base_model import CustomBaseModel
from database.models.profile import Profile
from database.models.musical_work import MusicalWork
from database.models.section import Section
from database.models.part import Part
from database.models.genre import Genre
from database.models.file import File
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
from database.models.validator import Validator
from database.models.software import Software
from database.models.encoder_validator_base_model \
    import EncoderValidatorBaseModel
from database.models.contributed_to import ContributedTo
from database.models.text_file import TextFile
from django.utils.translation import ugettext_lazy as _