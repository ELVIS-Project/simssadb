from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^list/$', views.MusicalWorkListView.as_view(), name='piece_list'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
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
        name='musicalwork-detail'),
    url(r'^parts/(?P<pk>[0-9]+)/$', views.PartDetail.as_view(),
        name='part-detail'),
    url(r'^sources/(?P<pk>[0-9]+)/$', views.SourceDetail.as_view(),
        name='source-detail'),
    url(r'^collections/(?P<pk>[0-9]+)/$',
        views.CollectionOfSourcesDetail.as_view(),
        name='collectionofsources-detail'),
    url(r'^institutions/(?P<pk>[0-9]+)/$', views.InstitutionDetail.as_view(),
        name='institution-detail')
    ]
