from django.db import models
from django.contrib.auth.models import User


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lecturer_name = models.CharField(max_length=50, null=False, unique = True)
    qualification = models.CharField(max_length=50, null=True, blank=True)
    TITLE_RANK_CHOICES = ((1, "Professor"), (2, "Assistant Professor"),
                          (3, 'Lecturer'), (4, 'Assistant Lecturer'),)
    title_rank = models.SmallIntegerField(
        choices=TITLE_RANK_CHOICES, default=4)
    department = models.CharField(max_length=50, null=True, blank=True)
    cv_link = models.URLField(max_length=255, null=True, blank=True, unique=True)
    gender = models.CharField(max_length=1, null=True, blank=True, choices=[
                              ('M', 'Male'), ('F', 'Female')])
    
    def __str__(self):
        return self.lecturer_name


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=155, unique=True)
    description = models.TextField(blank=True)
    prerequisites = models.TextField(blank=True)
    creation_date = models.DateField(auto_now_add = True)
    starting_date = models.DateField(blank=True, null=True)
    duration_days = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=7, decimal_places=0, blank=True, null=True)
    poster = models.CharField(max_length=255, blank=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course_name} ({self.course_id})"


class Student(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=14, unique=True) 
    PERSON_TYPE_CHOICES = [
        ('ST', 'Student'),
        ('EM', 'Employer'),
        ('OT', 'Others'),
    ]
    student_type = models.CharField(
        max_length=2,
        choices=PERSON_TYPE_CHOICES,
        default='OT',
    )
    courses = models.ManyToManyField(Course, blank=False)

    def __str__(self):
        return self.name
