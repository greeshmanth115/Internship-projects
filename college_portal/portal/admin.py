
from django.contrib import admin
from .models import Student, Faculty, Course, Subject, Marks, Attendance, Notice, Timetable

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Marks)
admin.site.register(Attendance)
admin.site.register(Notice)
admin.site.register(Timetable)