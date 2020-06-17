"""webapps URL Configuration

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
from django.urls import path, include
from musica_ludum import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.free_mode),
    path('accounts/login/', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('musica_ludum/', include('musica_ludum.urls')),
    path('piano/<str:audio>', views.get_key, name='piano'),
    path('record', views.record, name='record'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('getMIDI/<int:id>', views.get_midi, name='getMIDI'),
    path('renameMIDI/<int:id>', views.rename_midi, name='renameMIDI'),
    path('deleteMIDI/<int:id>', views.delete_midi, name='deleteMIDI'),
    path('simpleCompose/<int:id>', views.simple_compose, name='simpleCompose'),
    path('complexCompose/<int:id>', views.complex_compose, name='complexCompose'),
    path('simpleMIDI/<str:midi>', views.get_simple, name='get_simple'),
    path('complexMIDI/<str:midi>', views.get_complex, name='get_complex'),
]
