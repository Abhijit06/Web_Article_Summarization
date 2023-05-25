from django.contrib import admin
from django.urls import path
from newsletter_sum import views

urlpatterns = [
    path('newsletter/', views.index, name='newsletter_sum')
]
