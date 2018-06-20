from django.conf.urls import url
from django.conf.urls import include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'instruments', views.InstrumentViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'persons', views.PersonViewSet)
router.register(r'geographicareas', views.GeographicAreaViewSet)
router.register(r'sections', views.SectionViewSet)
router.register(r'musicalworks', views.MusicalWorkViewSet)
router.register(r'parts', views.PartViewSet)
router.register(r'sources', views.SourceViewSet)
router.register(r'collections', views.CollectionOfSourcesViewSet)
router.register(r'institutions', views.InstitutionViewSet)
router.register("person/search", views.PersonSearchView,
                base_name='person-search')

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^', include(router.urls))
    ]
