from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.free_mode, name='home'),
    path('game', views.game_mode, name='game'),
    path('singlegame', views.singlegame_mode, name='singlegame'),
    path('accounts/login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
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