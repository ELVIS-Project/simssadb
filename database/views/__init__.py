from database.views.postgres_search import PostgresSearchView
from database.views.front_end_views import AboutView, HomeView, SignUpView

from database.views.archive import ArchiveDetailView, ArchiveListView
from database.views.collection_of_sources import (
    CollectionOfSourcesDetailView,
    CollectionOfSourcesListView,
)
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
from database.views.file import FileDetailView
from database.views.genre_as_in_style import GenreAsInStyleDetailView
from database.views.genre_as_in_type import GenreAsInTypeDetailView
from database.views.geographic_area import GeographicAreaDetailView
from database.views.instrument import InstrumentDetailView
from database.views.musical_work import MusicalWorkDetailView, MusicalWorkListView
from database.views.part import PartDetailView
from database.views.person import PersonDetailView, PersonListView
from database.views.section import SectionDetailView
from database.views.source import SourceDetailView
