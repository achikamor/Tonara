from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', user_views.home_page, name='home-page'),
    path('school/', user_views.register_school, name='register-school'),
    path('teacher/', user_views.register_teacher, name='register-teacher'),
    path('student/', user_views.register_student, name="register-student"),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    path('teacher/add-student', user_views.add_student, name='add-student'),
    path('teacher/update-student', user_views.update_student, name='update-student'),
    path('teacher/delete-student', user_views.delete_student, name='delete-student'),
    path('teacher/get-students', user_views.get_students, name='get-students'),
    path('school/add-teacher', user_views.get_teachers, name='my-teachers'),
    path('school/add-teacher', user_views.add_teacher, name='add-teacher'),
    path('school/delete-teacher', user_views.delete_teacher, name='delete-teacher'),
    path('teacher/delete-teacher', user_views.teacher_delete_teacher, name='delete-teacher'),
    path('teacher/add-teacher', user_views.teacher_add_teacher, name='teacher-add-teacher'),
    path('teacher/get-teachers', user_views.teacher_get_teachers, name='get-teachers'),
    path('teacher/update-teacher', user_views.update_teacher, name='update-teacher'),

]
