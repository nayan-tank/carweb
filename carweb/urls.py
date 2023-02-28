"""first URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('admins/generate-report/', views.generate_report, name='generate_report'),
    path('admins/download-report/', views.download_report, name='download_report'),
    # path('report/', views.report, name='download_report'),
    path('', views.home, name='home'),
    path('', include('shop.urls')),

] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# add a flag for
# handling the 404 error
handler404 = 'shop.views.error_404_view'