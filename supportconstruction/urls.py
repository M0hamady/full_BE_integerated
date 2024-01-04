"""supportconstruction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from supportconstruction import settings
admin.site.site_header = 'Constructions'
admin.site.site_title = 'Administrator  '
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('project.urls')),
    path('website/', include('website.urls')),
    path('', include('client.urls')),
    path('markting/', include('markting.urls')),
    path('', include('manager.urls')),
    path('technical/', include('technical.urls')),
    path('designers/', include('designer.urls')),
    path('', include('teamview.urls')),
    path('project/', include('project.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)