from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='core-home'),
    path('course/', views.course, name='core-course'),
    path('course/<int:course_id>/', views.course_detail, name='core-course-detail'),
    path('lecturer/', views.lecturer, name='core-lecturer'),
    path('about/', views.about, name='core-about'),

]
