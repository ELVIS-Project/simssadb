from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from haystack.forms import FacetedSearchForm
from haystack.views import FacetedSearchView
import database.views as views
from database.views import (
    ArchiveAutocomplete,
    GeographicAreaAutocomplete,
    InstrumentAutocomplete,
    SoftwareAutocomplete,
    StyleAutocomplete,
    TypeAutocomplete,
    create_view,
    creation_view,
    file_creation_view,
    front_end_views,
    postgres_search,
)
from database.views.file_creation_view import FileCreationView

router = DefaultRouter()
router.register(r"instruments", views.InstrumentViewSet)
router.register(r"styles", views.GenreAsInStyleViewSet)
router.register(r"types", views.GenreAsInTypeViewSet)
router.register(r"persons", views.PersonViewSet)
router.register(r"geographicareas", views.GeographicAreaViewSet)
router.register(r"sections", views.SectionViewSet)
router.register(r"musicalworks", views.MusicalWorkViewSet)
router.register(r"parts", views.PartViewSet)
router.register(r"sources", views.SourceViewSet)
router.register(r"collections", views.CollectionOfSourcesViewSet)
router.register(r"institutions", views.InstitutionViewSet)
router.register(r"symbolicmusicfiles", views.SymbolicMusicFileViewSet)
router.register(r"extractedfeatures", views.ExtractedFeatureViewSet)
router.register(r"encoders", views.EncoderViewSet)
router.register(r"archives", views.ArchiveViewSet)
router.register(r"audiofiles", views.AudioFileViewSet)
router.register(r"contributions", views.ContributionViewSet)
router.register(r"corpora", views.ResearchCorpusViewSet)
router.register(r"software", views.SoftwareViewSet)
router.register(r"imagefiles", views.ImageFileViewSet)
router.register(r"textfiles", views.TextFileViewSet)
router.register(r"validators", views.ValidatorViewSet)
router.register(r"featuretypes", views.FeatureTypeViewSet)
router.register(r"experimentalstudies", views.ExperimentalStudyViewSet)

urlpatterns = [
    url(r"^$", front_end_views.HomeView.as_view(), name="home"),
    url(r"^about/$", front_end_views.AboutView.as_view(), name="about"),
    url(r"^", include(router.urls)),
    url(
        r"^search/$", views.postgres_search.PostgresSearchView.as_view(), name="search"
    ),
    url(r"^auto-fill/$", front_end_views.AutoFillView.as_view(), name="auto-fill"),
    url(
        r"musical_work",
        create_view.CreateMusicalWorkViewCustom.as_view(),
        name="musical_work",
    ),
    url(r"^create", creation_view.CreationView.as_view(), name="create"),
    url(
        r"^style-autocomplete/$",
        StyleAutocomplete.as_view(create_field="name"),
        name="style-autocomplete",
    ),
    url(
        r"^type-autocomplete/$",
        TypeAutocomplete.as_view(create_field="name"),
        name="type-autocomplete",
    ),
    url(
        r"^instrument-autocomplete/$",
        InstrumentAutocomplete.as_view(create_field="name"),
        name="instrument-autocomplete",
    ),
    url(
        r"^geographicarea-autocomplete/$",
        GeographicAreaAutocomplete.as_view(create_field="name"),
        name="geographicarea-autocomplete",
    ),
    url(
        r"^software-autocomplete/$",
        SoftwareAutocomplete.as_view(create_field="name"),
        name="software-autocomplete",
    ),
    url(
        r"^archive-autocomplete/$",
        ArchiveAutocomplete.as_view(create_field="name"),
        name="archive-autocomplete",
    ),
    url(
        r"file_create/",
        file_creation_view.FileCreationView.as_view(),
        name="file_creation",
    ),
    url(
        r"research_corpus",
        create_view.CreateResearchCorpus.as_view(),
        name="research_corpus",
    ),
]
