from django.contrib import admin
from .models import Lecturer, Course


class CourseAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Filter courses based on the lecturer for non-superusers
            qs = qs.filter(lecturer=request.user.lecturer)
        return qs
  

    def get_form(self, request, obj=None, **kwargs):
    # Customize the form based on the user's permissions
        if not request.user.is_superuser:
            self.exclude = ('lecturer',)
        else:
            self.exclude = ()
        return super().get_form(request, obj, **kwargs)
        

    def save_model(self, request, course, form, change):
        course.lecturer = request.user.lecturer
        super().save_model(request, course, form, change)

        
admin.site.register(Lecturer)
admin.site.register(Course, CourseAdmin)
