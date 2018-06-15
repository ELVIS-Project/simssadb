from django.conf.urls import url
from viapy.views import ViafLookup, ViafSearch
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^list/$', views.MusicalWorkListView.as_view(), name='piece_list'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^piece/new/$',views.CreatePieceView.as_view(), name='piece_new'),  # new post view
    url(r'^piece/(?P<pk>\d+)$',views.MusicalWorkDetailView.as_view(), name='musicalwork_detail'),
    url(r'signup/$', views.SignUp.as_view(), name="signup"),
    url(r'^suggest/$', ViafLookup.as_view(), name='suggest'),
    url(r'^suggest/person/$', ViafLookup.as_view(),
        {'nametype': 'personal'}, name='person-suggest'),
    url(r'^search/$', ViafSearch.as_view(), name='search'),
    url(r'^search/person/$', ViafSearch.as_view(),
        {'nametype': 'personal'}, name='person-search'),
    ]
