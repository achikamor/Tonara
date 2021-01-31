from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from .forms import *


def home_page(request):
    context = {}
    return render(request, 'users/homePage.html', context)


def register_student(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('USERNAME_FIELD')
            f_name = form.cleaned_data.get('first_name')
            l_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            psw = form.cleaned_data.get('password1')
            b_day = form.cleaned_data.get('birthday')
            teacher = form.cleaned_data.get('my_teacher')
            messages.success(request, f'Account created for student: {username}!')
            user = UserManage.objects.create_user(username, email, psw, is_student=True)
            user.save()
            student = Student(USERNAME_FIELD=username, first_name=f_name, last_name=l_name, email=email,
                              birthday=b_day, my_teacher=teacher, password=psw, user=user)
            student.save()
            return redirect('login')
    else:
        form = StudentRegisterForm()
    return render(request, "users/register.html", {'form': form})


def register_teacher(request):
    if request.method == "POST":
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('USERNAME_FIELD')
            f_name = form.cleaned_data.get('first_name')
            l_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            instrument = form.cleaned_data.get('instrument')
            school_id = form.cleaned_data.get('school_id')
            pos = form.cleaned_data.get('is_admin')
            psw = form.cleaned_data.get('password1')
            messages.success(request, f'Account created for teacher: {username}!')
            user = UserManage.objects.create_user(username, email, psw, is_teacher=True)
            user.save()
            teacher = Teacher(USERNAME_FIELD=username, first_name=f_name, last_name=l_name,
                              email=email, instrument=instrument, school_id=school_id, is_admin=pos,
                              password=psw, user=user)
            teacher.save()
            return redirect('login')
    else:
        form = TeacherRegisterForm()
    return render(request, "users/register.html", {'form': form})


def register_school(request):
    if request.method == "POST":
        form = SchoolRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('school_name')
            addr = form.cleaned_data.get('address')
            phone = form.cleaned_data.get('phone_number')
            psw = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('USERNAME_FIELD')
            messages.success(request, f'Account created for school: {username}!')
            user = UserManage.objects.create_user(username, form.cleaned_data.get('email'),
                                                  psw, is_school=True)

            user.save()

            school = School(USERNAME_FIELD=username, school_name=name, address=addr,
                            phone_number=phone, password=psw, user=user)
            school.save()
            return redirect('login')

    else:
        form = SchoolRegisterForm()
    return render(request, "users/register.html", {'form': form})


def add_student(request):
    teacher_id = request.user.id
    teacher = Teacher.objects.filter(pk=teacher_id).first()
    if request.method == "POST":
        if teacher.is_admin:
            form = StudentRegisterForm(request.POST)
        else:
            form = AddStudentForm(request.POST)
        if form.is_valid():
            assign_teacher = form.cleaned_data.get('my_teacher')
            if assign_teacher:
                if assign_teacher.school_id != teacher.school_id:
                    return HttpResponseNotFound('<h1>you are not allowed to add student to teacher who do not teaching in your school!</h1>')
                else:
                    final_teacher = assign_teacher
            else:
                final_teacher = teacher
            username = form.cleaned_data.get('USERNAME_FIELD')
            f_name = form.cleaned_data.get('first_name')
            l_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            psw = form.cleaned_data.get('password1')
            b_day = form.cleaned_data.get('birthday')
            user = UserManage.objects.create_user(username, email, psw, is_student=True)
            user.save()
            student = Student(USERNAME_FIELD=username, first_name=f_name, last_name=l_name, email=email,
                              birthday=b_day, my_teacher=final_teacher, password=psw, user=user)
            student.save()
            return redirect('home-page')
    else:
        if teacher.is_admin:
            form = StudentRegisterForm()
        else:
            form = AddStudentForm()
    return render(request, "users/add-student.html", {'form': form})


def update_student(request):
    teacher_id = request.user.id
    teacher = Teacher.objects.filter(pk=teacher_id).first()
    if request.method == "POST":
        if teacher.is_admin:
            form = UpdateStudentAdmin(request.POST)
        else:
            form = UpdateStudent(request.POST)
        if form.is_valid():
            assign_teacher = form.cleaned_data.get('my_teacher')
            if assign_teacher:
                if assign_teacher.school_id != teacher.school_id:
                    return HttpResponseNotFound(
                        '<h1>you are not allowed to add student to teacher who do not teaching in your school!</h1>')
                else:
                    final_teacher = assign_teacher
            else:
                final_teacher = teacher

            username = form.cleaned_data.get('USERNAME_FIELD')
            student = Student.objects.filter(USERNAME_FIELD=username).first()
            if student:
                f_name = form.cleaned_data.get('first_name')
                l_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                b_day = form.cleaned_data.get('birthday')
                student.first_name = f_name
                student.last_name = l_name
                student.email = email
                student.birthday = b_day
                student.my_teacher = final_teacher
                student.save()
                return redirect('home-page')
    else:
        if teacher.is_admin:
            form = UpdateStudentAdmin()
        else:
            form = UpdateStudent()
    return render(request, "users/update-student.html", {'form': form})


def delete_student(request):
    if request.method == "POST":
        form = DeleteStudent(request.POST)
        if form.is_valid():
            teacher_name = request.user.username
            teacher = Teacher.objects.filter(USERNAME_FIELD=teacher_name).first()
            student = form.cleaned_data.get('student')
            if student.my_teacher == teacher or (student.my_teacher.school_id == teacher.school_id and teacher.is_admin):
                student.user.delete()
            else:
                return HttpResponse('<div><h1>You are not allowed to delete this student</h1>'
                                    '<p>You may be a regular student or you are trying to delete a student from'
                                    ' another school</p></div>')
            return redirect('home-page')

    else:
        form = DeleteStudent()
    return render(request, "users/delete-student.html", {'form': form})


def get_students(request):
    teacher_name = request.user.username
    teacher = Teacher.objects.filter(USERNAME_FIELD=teacher_name).first()
    student_set = Student.objects.filter(my_teacher__in=Teacher.objects.filter(pk=teacher.pk))
    context = {'data': student_set}
    return render(request, "users/get-students.html", context)


def add_teacher(request):
    school_id = request.user.id
    if request.method == "POST":
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            adding_to = form.cleaned_data.get('school_id')
            if adding_to and adding_to == school_id:
                username = form.cleaned_data.get('USERNAME_FIELD')
                f_name = form.cleaned_data.get('first_name')
                l_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                psw = form.cleaned_data.get('password1')
                instrument = form.cleaned_data.get('instrument')
                is_admin = form.cleaned_data.get('is_admin')
                user = UserManage.objects.create_user(username, email, psw, is_teacher=True)
                user.save()
                teacher = Teacher(USERNAME_FIELD=username, first_name=f_name, last_name=l_name, email=email,
                                  instrument=instrument, is_admin=is_admin, password=psw, user=user, school_id=school_id)
                teacher.save()
                return redirect('home-page')
            else:
                return HttpResponse('<h1>You are not allowed to add teacher to another school</h1>')
    else:
        form = TeacherRegisterForm()
    return render(request, "users/add-teacher.html", {'form': form})


def delete_teacher(request):
    if request.method == "POST":
        form = DeleteTeacher(request.POST)
        if form.is_valid():
            school_id = request.user.id
            teacher_to_delete = form.cleaned_data.get('teacher')
            if teacher_to_delete.school_id == school_id:
                teacher_to_delete.user.delete()
            else:
                return HttpResponse('<h1>You are not allowed to delete this Teacher</h>')
            return redirect('home-page')

    else:
        form = DeleteTeacher()
    return render(request, "users/delete-student.html", {'form': form})


def teacher_add_teacher(request):
    if request.method == "POST":
        form = TeacherAddTeacherForm(request.POST)
        if form.is_valid():
            current_teacher_id = request.user.id
            current_teacher = Teacher.objects.filter(pk=current_teacher_id).first()
            if current_teacher.is_admin:
                username = form.cleaned_data.get('USERNAME_FIELD')
                f_name = form.cleaned_data.get('first_name')
                l_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                psw = form.cleaned_data.get('password1')
                instrument = form.cleaned_data.get('instrument')
                is_admin = form.cleaned_data.get('is_admin')
                user = UserManage.objects.create_user(username, email, psw, is_teacher=True)
                user.save()
                teacher = Teacher(USERNAME_FIELD=username, first_name=f_name, last_name=l_name, email=email,
                                  instrument=instrument, is_admin=is_admin, password=psw, user=user,
                                  school_id=current_teacher.school_id)
                teacher.save()
                return redirect('home-page')
            else:
                return HttpResponse('<h1>You are not allowed to add teacher to another school</h>')
            return redirect('home-page')

    else:
        form = TeacherAddTeacherForm()
    return render(request, "users/teacher-add-teacher.html", {'form': form})


def teacher_delete_teacher(request):
    if request.method == "POST":
        form = DeleteTeacher(request.POST)
        if form.is_valid():
            current_teacher_id = request.user.id
            current_teacher = Teacher.objects.filter(pk=current_teacher_id).first()
            teacher_to_delete = form.cleaned_data.get('teacher')
            if current_teacher.is_admin and teacher_to_delete.school_id == current_teacher.school_id:
                teacher_to_delete.user.delete()
            else:
                return HttpResponse('<h1>You are not allowed to delete this Teacher</h>')
            return redirect('home-page')

    else:
        form = DeleteTeacher()
    return render(request, "users/delete-teacher.html", {'form': form})


def teacher_get_teachers(request):
    teacher_id = request.user.id
    teacher = Teacher.objects.filter(pk=teacher_id).first()
    school_id = teacher.school_id
    teacher_set = Teacher.objects.filter(school_id__in=School.objects.filter(pk=school_id))
    context = {'data': teacher_set}
    return render(request, "users/get-teachers.html", context)


def update_teacher(request):
    curr_teacher_id = request.user.id
    curr_teacher = Teacher.objects.filter(pk=curr_teacher_id).first()
    if request.method == "POST":
        form = UpdateTeacherForm(request.POST)
        if form.is_valid():
            change_teacher = form.cleaned_data.get('teacher')
            if change_teacher and change_teacher.school_id == curr_teacher.school_id and curr_teacher.is_admin:
                f_name = form.cleaned_data.get('first_name')
                l_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                instrument = form.cleaned_data.get('instrument')
                is_admin = form.cleaned_data.get('is_admin')
                change_teacher.first_name = f_name
                change_teacher.last_name = l_name
                change_teacher.email = email
                change_teacher.instrument = instrument
                change_teacher.is_admin = is_admin
                change_teacher.save()
                return redirect('home-page')
            else:
                return HttpResponse('<h1>You are not allowed to update teacher from another school</h>')
    else:
        form = UpdateTeacherForm()
    return render(request, "users/update-teacher.html", {'form': form})


def get_teachers(request):
    school_id = request.user.id
    teacher_set = Teacher.objects.filter(school_id__in=School.objects.filter(pk=school_id))
    context = {'data': teacher_set}
    return render(request, "users/get-teachers.html", context)