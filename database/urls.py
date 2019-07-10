from django.conf.urls import include, url
from django.urls import path
from django.contrib.auth import views as auth_views
from database.views import (
    AboutView,
    HomeView,
    PostgresSearchView,
    SignUpView,
    CollectionOfSourcesDetailView,
    FileDetailView,
    GenreAsInStyleDetailView,
    GenreAsInTypeDetailView,
    InstrumentDetailView,
    MusicalWorkDetailView,
    PartDetailView,
    PersonDetailView,
    SectionDetailView,
    SourceDetailView,
)

urlpatterns = [
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
        "instruments/<int:pk>", InstrumentDetailView.as_view(), name="instrument-detail"
    ),
    ),
    url(r"^auto-fill/$", front_end_views.AutoFillView.as_view(), name="auto-fill"),
]    path("parts/<int:pk>", PartDetailView.as_view(), name="part-detail"),
    path("sections/<int:pk>", SectionDetailView.as_view(), name="section-detail"),
