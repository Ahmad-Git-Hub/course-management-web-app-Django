import datetime
from django.contrib import admin
from .models import Lecturer, Course

class LecturerAdmin(admin.ModelAdmin):
    list_display = ['lecturer_name', 'qualification', 'title_rank', 'gender', 'cv_link']
    ordering = ['title_rank']



class CourseAdmin(admin.ModelAdmin):

    list_display = ['course_id', 'course_name', 'starting_date', 'price', 'creation_date','is_approved', 'lecturer', 'days_since_creation']


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Filter courses based on the lecturer for non-superusers
            qs = qs.filter(lecturer=request.user.lecturer)
        return qs.order_by('starting_date')
  

    def get_form(self, request, obj=None, **kwargs):
    # Customize the form based on the user's permissions
        if not request.user.is_superuser:
            self.exclude = ('lecturer', 'creation_date')
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
  


        
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Course, CourseAdmin)
