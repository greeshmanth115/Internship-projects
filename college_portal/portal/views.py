
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Student, Faculty, Course, Subject, Marks, Attendance, Notice, Timetable
from .forms  import SignupForm, LoginForm


# HOME
def home(request):
    return render(request, 'portal/home.html')


# SIGN UP
def signup(request):
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        if Student.objects.filter(roll_number=data['roll_number']).exists():
            messages.error(request, 'Roll number already registered.')
            return render(request, 'portal/signup.html', {'form': form})
        user = User.objects.create_user(
            username=data['roll_number'],
            email=data['email'],
            password=data['password'],
        )
        Student.objects.create(
            user=user,
            name=data['name'],
            roll_number=data['roll_number'],
            branch=data['branch'],
            year=int(data['year']),
            semester=1,
            dob=data['dob'],
            email=data['email'],
            phone=data['phone'],
        )
        messages.success(request, 'Account created! Please login.')
        return redirect('login')
    return render(request, 'portal/signup.html', {'form': form})


# LOGIN
def login_view(request):
    error = None
    if request.method == 'POST':
        role     = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if role == 'student' and hasattr(user, 'student'):
                login(request, user); return redirect('student_dashboard')
            elif role == 'faculty' and hasattr(user, 'faculty'):
                login(request, user); return redirect('faculty_dashboard')
            elif role == 'admin' and user.is_staff:
                login(request, user); return redirect('admin_dashboard')
            else:
                error = f'You are not registered as {role}.'
        else:
            error = 'Invalid username or password.'
    return render(request, 'portal/login.html', {'error': error})


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')


# STUDENT DASHBOARD
@login_required(login_url='login')
def student_dashboard(request):
    student    = get_object_or_404(Student, user=request.user)
    marks      = Marks.objects.filter(student=student)
    attendance = Attendance.objects.filter(student=student)
    courses    = Course.objects.all()
    timetable  = Timetable.objects.filter(branch=student.branch, year=student.year)
    notices    = Notice.objects.all().order_by('-date')[:6]
    marks_data = [{'subject': m.subject.name,'internal': m.internal,'external': m.external,'total': m.total} for m in marks]
    att_data   = [{'subject': a.subject.name,'percentage': a.percentage} for a in attendance]
    return render(request, 'portal/student_dashboard.html', {
        'student': student, 'marks': marks_data, 'attendance': att_data,
        'courses': courses, 'timetable': timetable, 'notices': notices,
    })


# FACULTY DASHBOARD
@login_required(login_url='login')
def faculty_dashboard(request):
    faculty  = get_object_or_404(Faculty, user=request.user)
    subjects = Subject.objects.filter(faculty=faculty)
    students = Student.objects.filter(branch=faculty.department)
    return render(request, 'portal/faculty_dashboard.html', {
        'faculty': faculty, 'subjects': subjects, 'students': students,
    })


# SAVE MARKS
@login_required(login_url='login')
def save_marks(request):
    if request.method == 'POST':
        faculty  = get_object_or_404(Faculty, user=request.user)
        students = Student.objects.filter(branch=faculty.department)
        for s in students:
            subject_id = request.POST.get(f'subject_{s.id}')
            internal   = request.POST.get(f'internal_{s.id}', 0)
            external   = request.POST.get(f'external_{s.id}', 0)
            if subject_id:
                subject = get_object_or_404(Subject, id=subject_id)
                Marks.objects.update_or_create(student=s, subject=subject,
                    defaults={'internal': int(internal), 'external': int(external)})
        messages.success(request, 'Marks saved.')
    return redirect('faculty_dashboard')


# SAVE ATTENDANCE
@login_required(login_url='login')
def save_attendance(request):
    if request.method == 'POST':
        faculty  = get_object_or_404(Faculty, user=request.user)
        students = Student.objects.filter(branch=faculty.department)
        for s in students:
            subject_id = request.POST.get(f'att_subject_{s.id}')
            present    = request.POST.get(f'present_{s.id}', 0)
            total      = request.POST.get(f'total_{s.id}', 0)
            if subject_id:
                subject = get_object_or_404(Subject, id=subject_id)
                Attendance.objects.update_or_create(student=s, subject=subject,
                    defaults={'present': int(present), 'total': int(total)})
        messages.success(request, 'Attendance saved.')
    return redirect('faculty_dashboard')


# ADMIN DASHBOARD
@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login')
    return render(request, 'portal/admin_dashboard.html', {
        'students':       Student.objects.all(),
        'faculty_list':   Faculty.objects.all(),
        'courses':        Course.objects.all(),
        'total_students': Student.objects.count(),
        'total_faculty':  Faculty.objects.count(),
        'total_courses':  Course.objects.count(),
    })


# ADD STUDENT
@login_required(login_url='login')
def add_student(request):
    if not request.user.is_staff: return redirect('login')
    if request.method == 'POST':
        data = request.POST
        if not User.objects.filter(username=data['roll_number']).exists():
            user = User.objects.create_user(username=data['roll_number'], email=data['email'], password=data['password'])
            Student.objects.create(user=user, name=data['name'], roll_number=data['roll_number'],
                branch=data['branch'], year=int(data['year']), semester=int(data['semester']),
                dob=data['dob'], email=data['email'], phone=data['phone'])
            messages.success(request, 'Student added.')
        else:
            messages.error(request, 'Roll number already exists.')
    return redirect('admin_dashboard')


# EDIT STUDENT
@login_required(login_url='login')
def edit_student(request, pk):
    if not request.user.is_staff: return redirect('login')
    student = get_object_or_404(Student, id=pk)
    if request.method == 'POST':
        student.name=request.POST['name']; student.branch=request.POST['branch']
        student.year=int(request.POST['year']); student.semester=int(request.POST['semester'])
        student.email=request.POST['email']; student.phone=request.POST['phone']
        student.save(); messages.success(request, 'Student updated.')
        return redirect('admin_dashboard')
    return render(request, 'portal/edit_student.html', {'student': student})


# DELETE STUDENT
@login_required(login_url='login')
def delete_student(request, pk):
    if not request.user.is_staff: return redirect('login')
    student = get_object_or_404(Student, id=pk)
    student.user.delete()
    messages.success(request, 'Student deleted.')
    return redirect('admin_dashboard')


# ADD FACULTY
@login_required(login_url='login')
def add_faculty(request):
    if not request.user.is_staff: return redirect('login')
    if request.method == 'POST':
        data = request.POST
        if not User.objects.filter(username=data['employee_id']).exists():
            user = User.objects.create_user(username=data['employee_id'], email=data['email'], password=data['password'])
            Faculty.objects.create(user=user, name=data['name'], employee_id=data['employee_id'],
                department=data['department'], email=data['email'], phone=data['phone'])
            messages.success(request, 'Faculty added.')
        else:
            messages.error(request, 'Employee ID already exists.')
    return redirect('admin_dashboard')


# EDIT FACULTY
@login_required(login_url='login')
def edit_faculty(request, pk):
    if not request.user.is_staff: return redirect('login')
    faculty = get_object_or_404(Faculty, id=pk)
    if request.method == 'POST':
        faculty.name=request.POST['name']; faculty.department=request.POST['department']
        faculty.email=request.POST['email']; faculty.phone=request.POST['phone']
        faculty.save(); messages.success(request, 'Faculty updated.')
        return redirect('admin_dashboard')
    return render(request, 'portal/edit_faculty.html', {'faculty': faculty})


# DELETE FACULTY
@login_required(login_url='login')
def delete_faculty(request, pk):
    if not request.user.is_staff: return redirect('login')
    faculty = get_object_or_404(Faculty, id=pk)
    faculty.user.delete()
    messages.success(request, 'Faculty deleted.')
    return redirect('admin_dashboard')


# ADD COURSE
@login_required(login_url='login')
def add_course(request):
    if not request.user.is_staff: return redirect('login')
    if request.method == 'POST':
        name = request.POST['name']; code = request.POST['code']
        if not Course.objects.filter(code=code).exists():
            Course.objects.create(name=name, code=code)
            messages.success(request, 'Course added.')
        else:
            messages.error(request, 'Course code already exists.')
    return redirect('admin_dashboard')


# DELETE COURSE
@login_required(login_url='login')
def delete_course(request, pk):
    if not request.user.is_staff: return redirect('login')
    course = get_object_or_404(Course, id=pk)
    course.delete(); messages.success(request, 'Course deleted.')
    return redirect('admin_dashboard')