from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^list/$', views.MusicalWorkListView.as_view(), name='piece_list'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
<<<<<<< HEAD
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
=======
    url(r'^piece/new/$', views.CreatePieceView.as_view(), name='piece_new'),
    # new post view
    url(r'^musicalwork/(?P<pk>\d+)$', views.MusicalWorkDetailView.as_view(),
        name='musicalwork_detail'),
    url(r'signup/$', views.SignUp.as_view(), name="signup"),
    url(r'^instruments/(?P<pk>[0-9]+)/$', views.InstrumentDetail.as_view(),
        name='instrument-detail'),
    url(r'^genres/(?P<pk>[0-9]+)/$', views.GenreDetail.as_view(),
        name='genre-detail')
>>>>>>> 29c2e82... New: Added REST framework serializer, view and URL for Genre
    ]
