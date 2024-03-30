from datetime import date
from django.shortcuts import render
from .models import Lecturer, Course


def home(request):
    return render(request, 'core/index.html')


def course(request):
    lecturer_name = request.GET.get('lecturer_name', None) 
    today = date.today() 
    courses = Course.objects.filter(starting_date__gt=today)  
    if lecturer_name:
        courses = courses.filter(lecturer__lecturer_name__icontains=lecturer_name) 
    context = {'courses': courses}
    return render(request, 'core/course.html', context)

def lecturer(request):
    lecturers = Lecturer.objects.all()
    lecturer_name = request.GET.get('lecturer_name', '').lower()
    sort_by = request.GET.get('sort_by', '')
    if lecturer_name:
        lecturers = lecturers.filter(lecturer_name__icontains=lecturer_name)
    if sort_by:
        lecturers = lecturers.order_by(f"-{sort_by}" if sort_by == "qualification" else sort_by)
    context = {'lecturers': lecturers}
    return render(request, 'core/lecturer.html', context)
    
    