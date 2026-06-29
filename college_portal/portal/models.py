from django.db import models
from django.contrib.auth.models import User

#students
class Student(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    name        = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    branch      = models.CharField(max_length=20)
    year        = models.IntegerField()
    semester    = models.IntegerField(default=1)
    dob         = models.DateField()
    email       = models.EmailField()
    phone       = models.CharField(max_length=10)
    photo       = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

#faculty
class Faculty(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    name        = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    department  = models.CharField(max_length=20)
    email       = models.EmailField()
    phone       = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.employee_id})"

    class Meta:
        verbose_name_plural = "Faculty"

#cource
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

#subject
class Subject(models.Model):
    name    = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    course  = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

#marks
class Marks(models.Model):
    student  = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject  = models.ForeignKey(Subject, on_delete=models.CASCADE)
    internal = models.IntegerField(default=0)
    external = models.IntegerField(default=0)

    @property
    def total(self):
        return self.internal + self.external

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}"

    class Meta:
        unique_together = ('student', 'subject')
        verbose_name_plural = "Marks"

#attendence
class Attendance(models.Model):
    student    = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    subject    = models.ForeignKey(Subject, on_delete=models.CASCADE)
    present    = models.IntegerField(default=0)
    total      = models.IntegerField(default=0)

    @property
    def percentage(self):
        if self.total == 0:
            return 0
        return round((self.present / self.total) * 100, 1)

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}"

    class Meta:
        unique_together = ('student', 'subject')
        verbose_name_plural = "Attendance"

#notice
class Notice(models.Model):
    title   = models.CharField(max_length=200)
    content = models.TextField()
    date    = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

#timetable
class Timetable(models.Model):
    DAYS = [
        ('Monday','Monday'), ('Tuesday','Tuesday'), ('Wednesday','Wednesday'),
        ('Thursday','Thursday'), ('Friday','Friday'), ('Saturday','Saturday'),
    ]
    branch  = models.CharField(max_length=20)
    year    = models.IntegerField()
    day     = models.CharField(max_length=10, choices=DAYS)
    slot1   = models.CharField(max_length=50, blank=True)
    slot2   = models.CharField(max_length=50, blank=True)
    slot3   = models.CharField(max_length=50, blank=True)
    slot4   = models.CharField(max_length=50, blank=True)
    slot5   = models.CharField(max_length=50, blank=True)
    slot6   = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.branch} Y{self.year} - {self.day}"
    
class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registrations')
    course  = models.ForeignKey(Course, on_delete=models.CASCADE)
    registered_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"
    
class DailyAttendance(models.Model):
    student  = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='daily_attendance')
    subject  = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date     = models.DateField()
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.date}"