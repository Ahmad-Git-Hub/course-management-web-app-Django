from django.shortcuts import render


def home(request):
    return render(request, 'core/index.html')


def course(request):
    
    return render(request, 'core/course.html',)


def lecturer(request):
    
    
    return render(request, 'core/lecturer.html',)