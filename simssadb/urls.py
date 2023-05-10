from django.conf import settings
from django.conf.urls.static import static

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
from django.urls import path, re_path
from django.conf.urls import include
from django.contrib.auth import views
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
import debug_toolbar

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    re_path(r"", include("database.urls")),
    re_path(r"accounts/login/$", views.LoginView, name="login"),
    re_path(
        r"accounts/logout/$", views.LogoutView, name="logout", kwargs={"next_page": "/"}
    ),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns
