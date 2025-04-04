"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from tutorial import view
from tutorial.view import  HomePageView, AboutPageView, CarrerasCreateViewPage, CarrerasEditarViewPage, CarrerasEliminarViewPage, WebSocketView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', view.index, name='index'),
    path('',HomePageView.as_view(),name='home'),
    path('about/',AboutPageView.as_view(),name='about'),
    path('carrera/crear',CarrerasCreateViewPage.as_view(), name='carrera_crear'),
    path('carreras/editar/<int:pk>/',CarrerasEditarViewPage.as_view(), name='editar_carrera'),
    path('carreras/eliminar/<int:pk>/',CarrerasEliminarViewPage.as_view(), name='eliminar_carrera'),
    path('login/',auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name="login.hmtl"), name='logout'),
    path('websocket/', WebSocketView.as_view(), name='websocket'),
]
