from django.conf.urls import include, url
from django.urls import path
from django.contrib.auth import views as auth_views
from database.views import (
    AboutView,
    HomeView,
    PostgresSearchView,
    SignUpView,
    ArchiveDetailView,
    ArchiveListView,
    CollectionOfSourcesDetailView,
    FileDetailView,
    GeographicAreaDetailView,
    GenreAsInStyleDetailView,
    GenreAsInTypeDetailView,
    InstrumentDetailView,
    MusicalWorkDetailView,
    MusicalWorkListView,
    PartDetailView,
    PersonDetailView,
    PersonListView,
    SectionDetailView,
    SourceDetailView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("search/", PostgresSearchView.as_view(), name="search"),
    path("archives/<int:pk>", ArchiveDetailView.as_view(), name="archive-detail"),
    path("archives/", ArchiveListView.as_view(), name="archive-list"),
    path(
        "collectionsofsources/<int:pk>",
        CollectionOfSourcesDetailView.as_view(),
        name="collectionofsources-detail",
    ),
    path("files/<int:pk>", FileDetailView.as_view(), name="file-detail"),
    path(
        "styles/<int:pk>",
        GenreAsInStyleDetailView.as_view(),
        name="genreasinstyle-detail",
    ),
    path(
        "types/<int:pk>", GenreAsInTypeDetailView.as_view(), name="genreasintype-detail"
    ),
    path(
        "areas/<int:pk>",
        GeographicAreaDetailView.as_view(),
        name="geographicarea-detail",
    ),
    path(
        "instruments/<int:pk>", InstrumentDetailView.as_view(), name="instrument-detail"
    ),
    path(
        "musicalworks/<int:pk>",
        MusicalWorkDetailView.as_view(),
        name="musicalwork-detail",
    ),
    path("musicalworks/", MusicalWorkListView.as_view(), name="musicalwork-list"),
    path("parts/<int:pk>", PartDetailView.as_view(), name="part-detail"),
    path("persons/<int:pk>", PersonDetailView.as_view(), name="person-detail"),
    path("persons/", PersonListView.as_view(), name="person-list"),
    path("sections/<int:pk>", SectionDetailView.as_view(), name="section-detail"),
    path("sources/<int:pk>", SourceDetailView.as_view(), name="source-detail"),
]
