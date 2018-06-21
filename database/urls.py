from django.conf.urls import url
from django.conf.urls import include
from . import views
from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
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
    url(r'^', include(router.urls)),
    url(r'^general/?$', views.GeneralSearch.as_view(), name='general')
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^piece/new/$',views.CreatePieceView.as_view(), name='piece_new'),  # new post view
    url(r'^piece/(?P<pk>\d+)$',views.MusicalWorkDetailView.as_view(), name='musicalwork_detail'),
    #url(r'^signup/$', views.SignUp.as_view(), name="signup"),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),  # when the user click the activation url in the email, this view will be triggered
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'), # Using Django built-in authentication functions where you dont need to provide view functions, just specify the corresponding templates
    url(r'^piece/new/$', views.CreatePieceView.as_view(), name='piece_new'),
    # new post view
    # url(r'^musicalwork/(?P<pk>\d+)$', views.MusicalWorkDetailView.as_view(),
    #     name='musicalwork_detail'),
    url(r'signup/$', views.SignUp.as_view(), name="signup"),
    url(r'^instruments/(?P<pk>[0-9]+)/$', views.InstrumentDetail.as_view(),
        name='instrument-detail'),
    url(r'^genres/(?P<pk>[0-9]+)/$', views.GenreDetail.as_view(),
        name='genre-detail'),
    url(r'^persons/(?P<pk>[0-9]+)/$', views.PersonDetail.as_view(),
        name='person-detail'),
    url(r'^geographicareas/(?P<pk>[0-9]+)/$',
        views.GeographicAreaDetail.as_view(),
        name='geographicarea-detail'),
    url(r'^sections/(?P<pk>[0-9]+)/$', views.SectionDetail.as_view(),
        name='section-detail'),
    url(r'^musicalworks/(?P<pk>[0-9]+)/$', views.MusicalWorkDetail.as_view(),
        name='musicalwork-detail')
    url(r'^parts/(?P<pk>[0-9]+)/$', views.PartDetail.as_view(),
        name='part-detail'),
    url(r'^sources/(?P<pk>[0-9]+)/$', views.SourceDetail.as_view(),
        name='source-detail'),
    url(r'^collections/(?P<pk>[0-9]+)/$',
        views.CollectionOfSourcesDetail.as_view(),
        name='collectionofsources-detail'),
    url(r'^institutions/(?P<pk>[0-9]+)/$', views.InstitutionDetail.as_view(),
        name='institution-detail')
    url(r'^', include(router.urls))
    ]
