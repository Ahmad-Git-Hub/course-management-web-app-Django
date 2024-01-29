from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='core-home'),
    path('course/', views.course, name='core-course'),
    path('lecturer/', views.lecturer, name='core-lecturer'),
]
