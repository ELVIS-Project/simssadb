from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^list/$', views.MusicalWorkListView.as_view(), name='piece_list'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^piece/new/$',views.CreatePieceView.as_view(), name='piece_new'),  # new post view
    url(r'^piece/(?P<pk>\d+)$',views.MusicalWorkDetailView.as_view(), name='musicalwork_detail'),
    url(r'signup/$', views.SignUp.as_view(), name="signup"),
    url(r'search/$', views.FullTextSearch.as_view(), name='search'),
    url(r'searchresult', views.FullTextSearchResult.as_view(),
        name='search_result')
    ]
