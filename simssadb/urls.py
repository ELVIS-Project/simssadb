"""simssadb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('database.urls')),
    #url(r'^viaf/', include(('viapy.urls', 'viapy'), namespace='viaf')),
    #url(r'', include('viapy.urls')),
    url(r'accounts/login/$', views.login, name='login'),  # this goes to login.html page, see the source code
    url(r'accounts/logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
    # when you log out, it goes to home
]
