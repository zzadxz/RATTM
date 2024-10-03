"""
URL configuration for RattmWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.views.generic import RedirectView
from routers import router
from .views import testing


urlpatterns = [
    path('admin/', admin.site.urls),
    # defines a path that includes all URLs from the router, prefixed with 'api/'
    #path('api/', include((router.urls, 'core_api', 'transaction.urls'), namespace='core_api')),
    path('api/', include('transaction.urls')),
    path('', testing),
]