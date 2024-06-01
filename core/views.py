from datetime import date
from django.shortcuts import render, get_object_or_404
from .models import Lecturer, Course

def home(request):
    context = {'current_page': 'home'}
    return render(request, 'core/home.html', context)

def about(request):
    context = {'current_page': 'about'}
    return render(request, 'core/about.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Course, course_id=course_id, is_approved=True)
    context = {'course': course, 'current_page': 'course_detail'}
    return render(request, 'core/course_detail.html', context)

def course(request):
    course_name = request.GET.get('course_name', None) 
    today = date.today() 
    courses = Course.objects.filter(starting_date__gt=today, is_approved=True)  
    if course_name:
        courses = courses.filter(course_name__icontains=course_name) 
    context = {'courses': courses, 'current_page': 'course'}
    return render(request, 'core/course.html', context)

def lecturer(request):
    lecturers = Lecturer.objects.all()
    lecturer_name = request.GET.get('lecturer_name', '').lower()
    sort_by = request.GET.get('sort_by', '')
    if lecturer_name:
        lecturers = lecturers.filter(lecturer_name__icontains=lecturer_name)
    if sort_by:
        lecturers = lecturers.order_by(f"-{sort_by}" if sort_by == "qualification" else sort_by)
    context = {'lecturers': lecturers, 'current_page': 'lecturer'}
    return render(request, 'core/lecturer.html', context)
    
    
def lecturer_course(request, lecturer_name):
    today = date.today() 
    courses = Course.objects.filter(starting_date__gt=today, is_approved=True, lecturer__lecturer_name=lecturer_name)
    lecturer_name = request.GET.get('lecturer_name', None) 
    context = {'current_page': 'lecturer_course', 'courses': courses, 'lecturer_name' : lecturer_name}
    return render(request, 'core/lecturer_course.html', context)