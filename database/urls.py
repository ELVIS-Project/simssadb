from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from database.views import (
    postgres_search,
    front_end_views
)


urlpatterns = [
    url(r"^$", front_end_views.HomeView.as_view(), name="home"),
    url(r"^about/$", front_end_views.AboutView.as_view(), name="about"),
    url(
        r"^search/$", postgres_search.PostgresSearchView.as_view(), name="search"
    ),
    url(r"^auto-fill/$", front_end_views.AutoFillView.as_view(), name="auto-fill"),
]