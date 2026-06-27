# portal/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.home,              name='home'),
    path('signup/',                   views.signup,            name='signup'),
    path('login/',                    views.login_view,        name='login'),
    path('logout/',                   views.logout_view,       name='logout'),

    path('student/',                  views.student_dashboard, name='student_dashboard'),

    path('faculty/',                  views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/marks/',            views.save_marks,        name='save_marks'),
    path('faculty/attendance/',       views.save_attendance,   name='save_attendance'),

    path('admin-panel/',                          views.admin_dashboard,  name='admin_dashboard'),
    path('admin-panel/student/add/',              views.add_student,      name='add_student'),
    path('admin-panel/student/edit/<int:pk>/',    views.edit_student,     name='edit_student'),
    path('admin-panel/student/delete/<int:pk>/',  views.delete_student,   name='delete_student'),
    path('admin-panel/faculty/add/',              views.add_faculty,      name='add_faculty'),
    path('admin-panel/faculty/edit/<int:pk>/',    views.edit_faculty,     name='edit_faculty'),
    path('admin-panel/faculty/delete/<int:pk>/',  views.delete_faculty,   name='delete_faculty'),
    path('admin-panel/course/add/',               views.add_course,       name='add_course'),
    path('admin-panel/course/delete/<int:pk>/',   views.delete_course,    name='delete_course'),
]