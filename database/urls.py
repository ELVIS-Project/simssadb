from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

import database.views as views
from database.views import front_end_views


router = DefaultRouter()
router.register(r'instruments', views.InstrumentViewSet)
router.register(r'styles', views.GenreAsInStyleViewSet)
router.register(r'types', views.GenreAsInTypeViewSet)
router.register(r'persons', views.PersonViewSet)
router.register(r'geographicareas', views.GeographicAreaViewSet)
router.register(r'sections', views.SectionViewSet)
router.register(r'musicalworks', views.MusicalWorkViewSet)
router.register(r'parts', views.PartViewSet)
router.register(r'sources', views.SourceViewSet)
router.register(r'collections', views.CollectionOfSourcesViewSet)
router.register(r'institutions', views.InstitutionViewSet)
router.register(r'symbolicmusicfiles', views.SymbolicMusicFileViewSet)
router.register(r'extractedfeatures', views.ExtractedFeatureViewSet)
router.register(r'encoders', views.EncoderViewSet)
router.register(r'archives', views.ArchiveViewSet)
router.register(r'audiofiles', views.AudioFileViewSet)
router.register(r'contributions', views.ContributionViewSet)
router.register(r'corpora', views.ResearchCorpusViewSet)
router.register(r'software', views.SoftwareViewSet)
router.register(r'imagefiles', views.ImageFileViewSet)
router.register(r'textfiles', views.TextFileViewSet)
router.register(r'validators', views.ValidatorViewSet)
router.register(r'featuretypes', views.FeatureTypeViewSet)
router.register(r'experimentalstudies', views.ExperimentalStudyViewSet)

urlpatterns = [
    url(r'^$', front_end_views.HomeView.as_view(), name='home'),
    url(r'^about/$', front_end_views.AboutView.as_view(), name='about'),
    url(r'^piece/new/$', front_end_views.CreatePieceView.as_view(),
        name='piece_new'),
    url(r'^signup/$', front_end_views.signup, name='signup'),
    url(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        front_end_views.activate, name='activate'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^', include(router.urls)),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^auto-fill/$', front_end_views.AutoFillView.as_view(), name='auto-fill'),
    ]
