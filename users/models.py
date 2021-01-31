from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser


class UserManage(AbstractUser):
    is_school = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class School(models.Model):
    USERNAME_FIELD = models.CharField(max_length=50, default="def_user")
    school_name = models.CharField(max_length=100, default="Mekif")
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50, default="555555")
    password = models.CharField(max_length=24, default="1234")
    user = models.OneToOneField(UserManage, on_delete=models.CASCADE, primary_key=True, default=None)

    def get_name(self):
        return self.school_name

    def get_address(self):
        return self.address

    def get_phone_number(self):
        return self.phone_number

    def set_school_name(self, name):
        self.school_name = name

    def set_address(self, addr):
        self.address = addr

    def set_phone_number(self, phone):
        self.phone_number = phone

    def set_password(self, psw):
        self.password = psw

    def __str__(self):
        return self.get_name() + " located in: " + self.get_address() + "\nphone number: " \
               + self.get_phone_number()


class Teacher(models.Model):
    USERNAME_FIELD = models.CharField(max_length=50, default="def_user")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    teaching_since = models.DateField(auto_now_add=True)     #saving the time of creation of the teacher in the db
    instrument = models.CharField(max_length=100)
    school_id = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=24, default="1234")
    user = models.OneToOneField(UserManage, on_delete=models.CASCADE, primary_key=True, default=None)

    def get_name(self):
        return self.first_name + " " + self.last_name

    def get_starting_date(self):
        return self.teaching_since

    def get_email(self):
        return self.email

    def get_instrument(self):
        return self.instrument

    def set_first_name(self, f_name):
        self.first_name = f_name

    def set_last_name(self, l_name):
        self.last_name = l_name

    def set_instrument(self, inst):
        self.instrument = inst

    def set_email(self, mail):
        self.email = mail

    def set_password(self, psw):
        self.password = psw

    def set_is_admin(self, pos):
        self.is_admin = pos

    def create_student(self, first, last, email, birthday):
        new_student = Student(_first_name=first, _last_name=last, _email=email, _birthday=birthday, _my_teacher=self)
        new_student.save()

    def my_students(self):
        my_students = Student.objects.filter(_my_teacher=self)
        return my_students

    def __str__(self):
        pos = " is Admin " if self.is_admin else " is regular teacher "
        return self.get_name() + pos + "in school id " + str(self.school_id) + " and teaching " + self.instrument


class Student(models.Model):
    USERNAME_FIELD = models.CharField(max_length=50, default="def_user")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    student_since = models.DateField(auto_now_add=True)     #saving the time of creation of the student in the db
    birthday = models.DateField(default=(datetime.date(1993, 6, 21)))
    my_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=None)    #when the teacher is deleted,
    password = models.CharField(max_length=24, default="1234")                                                       # delete all the studetns that reffers to her
    user = models.OneToOneField(UserManage, on_delete=models.CASCADE, primary_key=True, default=None)

    def get_name(self):
        return self.first_name + " " + self.last_name

    def get_starting_date(self):
        return self.student_since

    def get_email(self):
        return self.email

    def get_birthday(self):
        return self.birthday

    def get_teacher_name(self):
        return self.my_teacher.get_name()

    def set_first_name(self, f_name):
        self.first_name = f_name

    def set_last_name(self, l_name):
        self.first_name = l_name

    def set_email(self, mail):
        self.first_name = mail

    def set_password(self, psw):
        self.password = psw

    def set_birthday(self, b_day):
        self.birthday = b_day

    def set_my_teacher(self, t):
        self.my_teacher = t

    def __str__(self):
        return self.get_name() + " is student of " + self.get_teacher_name()\
                 + " since: " + str(self.get_starting_date()) + " was born at " + str(self.get_birthday())



