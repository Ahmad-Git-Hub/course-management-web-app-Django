from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='core-home'),
    path('course/', views.course, name='core-course'),
    path('course/<int:course_id>/', views.course_detail, name='core-course-detail'),  # new line
    path('lecturer/', views.lecturer, name='core-lecturer'),
]
