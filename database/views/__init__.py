from database.views.search import SearchView
from database.views.front_end_views import AboutView, HomeView, SignUpView
from database.views.archive import ArchiveDetailView, ArchiveListView
from database.views.contribution_musical_work import (
    ContributionMusicalWorkDetailView,
    ContributionMusicalWorkListView,
)
from database.views.creation_view import CreationView # testing
from database.views.encoding_workflow import (
    EncodingWorkflowDetailView,
    EncodingWorkflowListView,
)
from database.views.experimental_study import (
    ExperimentalStudyDetailView,
    ExperimentalStudyListView,
)
from database.views.extracted_feature import (
    ExtractedFeatureDetailView,
    ExtractedFeatureListView,
)
from database.views.feature_file import FeatureFileDetailView, FeatureFileListView
from database.views.feature_type import FeatureTypeDetailView, FeatureTypeListView
from database.views.file import FileDetailView, FileListView
from database.views.file_creation_view import FileCreationView
from database.views.genre_as_in_style import (
    GenreAsInStyleDetailView,
    GenreAsInStyleListView,
)
from database.views.genre_as_in_type import (
    GenreAsInTypeDetailView,
    GenreAsInTypeListView,
)
from database.views.geographic_area import (
    GeographicAreaDetailView,
    GeographicAreaListView,
)
from database.views.instrument import InstrumentDetailView, InstrumentListView
from database.views.language import LanguageDetailView, LanguageListView
from database.views.musical_work import MusicalWorkDetailView, MusicalWorkListView
from database.views.create_view import CreateMusicalWorkViewCustom
from database.views.part import PartDetailView, PartListView
from database.views.person import PersonDetailView, PersonListView
from database.views.research_corpus import (
    ResearchCorpusDetailView,
    ResearchCorpusListView,
)
from database.views.section import SectionDetailView, SectionListView
from database.views.software import SoftwareDetailView, SoftwareListView
from database.views.source import SourceDetailView, SourceListView
from database.views.type_of_section import (
    TypeOfSectionDetailView,
    TypeOfSectionListView,
)
from database.views.validation_worflow import (
    ValidationWorkFlowDetailView,
    ValidationWorkFlowListView,
)
from database.views.download import (
    download_content_file,
    download_feature_file,
    download_cart,
)
from database.views.cart import CartView, add_to_cart, remove_from_cart, clear_cart
from database.views.autocomplete_views import (
    StyleAutocomplete, TypeAutocomplete, GeographicAreaAutocomplete,
    InstrumentAutocomplete, SoftwareAutocomplete,
    ArchiveAutocomplete, FileAutocomplete, MusicalWorkAutocomplete, PersonAutocomplete
)
from database.views.autocomplete_create import create_type, create_style, create_geographic_area, create_instrument