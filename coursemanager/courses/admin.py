from django.contrib import admin
from .models import Department, Course, Student, Enrollment

# Register Department
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head_of_dept', 'budget']
    search_fields = ['name']


# Register Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credits', 'department']
    search_fields = ['name', 'code']
    list_filter = ['department']


# Register Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'department']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['department']


# Register Enrollment
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date', 'grade']
    list_filter = ['course']
    