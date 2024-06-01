import datetime
from django.contrib import admin
from .models import Lecturer, Course, Student
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'is_superuser', 'is_staff', 'is_active', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class LecturerAdmin(admin.ModelAdmin):
    list_display = ['lecturer_name', 'qualification', 'title_rank', 'gender', 'cv_link']
    ordering = ['title_rank']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(id=request.user.id)
        return queryset
   


class CourseAdmin(admin.ModelAdmin):

    list_display = ['course_id', 'course_name', 'starting_date', 'price', 'creation_date','is_approved', 'lecturer', 'days_since_creation']
    actions = ['approve_courses', 'disapprove_courses']


    def approve_courses(self, request, queryset):
        queryset.update(is_approved=True)
    approve_courses.short_description = "Approve selected courses"

    def disapprove_courses(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_courses.short_description = "Disapprove selected courses"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Filter courses based on the lecturer for non-superusers
            qs = qs.filter(lecturer=request.user.lecturer)
        return qs.order_by('starting_date')
  

    def get_form(self, request, obj=None, **kwargs):
    # Customize the form based on the user's permissions
        if not request.user.is_superuser:
            self.exclude = ('lecturer', 'creation_date', 'is_approved')
        else:
            self.exclude = ()
        return super().get_form(request, obj, **kwargs)
        

    def save_model(self, request, course, form, change):
        if request.user.is_superuser:
            course.lecturer = form.cleaned_data['lecturer']
        else:
            course.lecturer = request.user.lecturer
        super().save_model(request, course, form, change)

   
    def days_since_creation(self, course):
        days = (datetime.date.today() - course.creation_date).days
        return days
    
    days_since_creation.short_description = "Days Since Creation"

    def __str__(self):
        return f"{self.course_name} ({self.course_id}, {self.starting_date}, {self.price})"



class StudentAdmin(admin.ModelAdmin):
    filter_horizontal = ('courses',)
    list_display = ('name', 'email', 'phone_number', 'student_type', 'registration_date', 'view_courses_link')

    def view_courses_link(self, obj):
        url = reverse("admin:core_student_change", args=[obj.pk])
        return format_html('<a href="{}">View Courses</a>', url)
    view_courses_link.short_description = 'Courses'


        
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)

admin.site.site_header = "Continuous Education"
admin.site.site_title = "CT Admin"
admin.site.index_title = "Welcome Continuous Education manager"
