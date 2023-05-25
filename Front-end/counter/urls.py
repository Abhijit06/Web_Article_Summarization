from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('', views.Signup, name='signup'),
    path('about', views.about, name='about'),
    path('login/', views.Login, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('summarize', views.summarize, name='summarize'),
    path('speech', views.speech, name='speech'),
    path('newsletter', views.newsletter, name='newsletter'),
    path('email', views.email, name='email'),
    path('audio', views.audio, name='audio'),
    path('team', views.team, name='team'),
    path('image', views.image, name='image'),
]
