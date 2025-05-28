"""
URL configuration for lliga project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.urls import path, include
from . import views

app_name = "futbol"
urlpatterns = [
  path("classificacio", views.classificacio_menu, name="classificacio_menu"),
  path("taula_partits", views.taula_partits_menu, name="taula_partits_menu"),
  path("taula_partits/<int:lliga_id>/", views.taula_partits, name="taula_partits"),
  path("classificacio/<int:lliga_id>/", views.classificacio, name="classificacio"),
]
