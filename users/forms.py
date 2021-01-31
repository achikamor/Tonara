from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class TeacherRegisterForm(UserCreationForm):
    USERNAME_FIELD = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    teaching_since = forms.DateField(initial=datetime.date.today)
    instrument = forms.CharField(max_length=100)
    school_id = forms.IntegerField(initial=0)
    is_admin = forms.BooleanField(required=False)

    class Meta:
        model = UserManage
        fields = ['USERNAME_FIELD', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'instrument', 'school_id', 'is_admin']


class StudentRegisterForm(UserCreationForm):
    USERNAME_FIELD = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    student_since = forms.DateField(initial=datetime.date.today)
    birthday = forms.DateField(initial=datetime.date.today)
    my_teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

    class Meta:
        model = UserManage
        fields = ['USERNAME_FIELD', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'birthday', 'my_teacher']


class SchoolRegisterForm(UserCreationForm):
    USERNAME_FIELD = forms.CharField(max_length=50)
    school_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=50)

    class Meta:
        model = UserManage
        fields = ['USERNAME_FIELD', 'school_name', 'address', 'phone_number']


class AddStudentForm(UserCreationForm):
    USERNAME_FIELD = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    student_since = forms.DateField(initial=datetime.date.today)
    birthday = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = UserManage
        fields = ['USERNAME_FIELD', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'birthday']


class UpdateStudent(UserChangeForm):
    USERNAME_FIELD = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    birthday = forms.DateField()

    class Meta:
        model = Student
        fields = ['USERNAME_FIELD', 'first_name', 'last_name', 'email', 'birthday']


class UpdateStudentAdmin(UserChangeForm):
    USERNAME_FIELD = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    birthday = forms.DateField()
    my_teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

    class Meta:
        model = Student
        fields = ['USERNAME_FIELD', 'first_name', 'last_name', 'email', 'birthday', 'my_teacher']


class DeleteStudent(UserChangeForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all())

    class Meta:
        model = Student
        fields = ['student']


class AddTeacherForm(UserCreationForm):
    USERNAME_FIELD = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    teaching_since = forms.DateField(initial=datetime.date.today)
    instrument = forms.CharField(max_length=100)
    school_id = forms.IntegerField(initial=0)
    is_admin = forms.BooleanField(required=False)

    class Meta:
        model = UserManage
        fields = ['USERNAME_FIELD', 'first_name', 'last_name', 'email', 'password1',
                  'password2', 'instrument', 'school_id', 'is_admin']


class DeleteTeacher(UserChangeForm):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

    class Meta:
        model = Teacher
        fields = ['teacher']


class TeacherAddTeacherForm(UserCreationForm):
    USERNAME_FIELD = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    teaching_since = forms.DateField(initial=datetime.date.today)
    instrument = forms.CharField(max_length=100)
    is_admin = forms.BooleanField(required=False)

    class Meta:
        model = UserManage
        fields = ['USERNAME_FIELD', 'first_name', 'last_name', 'email', 'password1',
                  'password2', 'instrument', 'is_admin']


class UpdateTeacherForm(UserChangeForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    instrument = forms.CharField()
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())
    is_admin = forms.BooleanField(required=False)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'instrument', 'teacher', 'is_admin']