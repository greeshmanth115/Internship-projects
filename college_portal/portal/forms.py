# portal/forms.py

from django import forms
from .models import Student, Faculty, Course


class SignupForm(forms.Form):
    name             = forms.CharField(max_length=100)
    roll_number      = forms.CharField(max_length=20)
    branch           = forms.ChoiceField(choices=[
                           ('CSE','CSE'),('ECE','ECE'),
                           ('EEE','EEE'),('MECH','MECH'),('CIVIL','CIVIL')
                       ])
    year             = forms.ChoiceField(choices=[('1','1'),('2','2'),('3','3'),('4','4')])
    dob              = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    email            = forms.EmailField()
    phone            = forms.CharField(max_length=10)
    password         = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        pwd  = cleaned.get('password')
        cpwd = cleaned.get('confirm_password')
        if pwd and cpwd and pwd != cpwd:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned


class LoginForm(forms.Form):
    ROLES = [('student','Student'),('faculty','Faculty'),('admin','Admin')]
    role     = forms.ChoiceField(choices=ROLES)
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)