# Generated by Django 3.1.5 on 2021-01-29 11:07

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserManage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_school', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('USERNAME_FIELD', models.CharField(default='def_user', max_length=50)),
                ('school_name', models.CharField(default='Mekif', max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone_number', models.CharField(default='555555', max_length=50)),
                ('password', models.CharField(default='1234', max_length=24)),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.usermanage')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('USERNAME_FIELD', models.CharField(default='def_user', max_length=50)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('teaching_since', models.DateField(auto_now_add=True)),
                ('instrument', models.CharField(max_length=100)),
                ('school_id', models.IntegerField(default=0)),
                ('is_admin', models.BooleanField(default=False)),
                ('password', models.CharField(default='1234', max_length=24)),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.usermanage')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('USERNAME_FIELD', models.CharField(default='def_user', max_length=50)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('student_since', models.DateField(auto_now_add=True)),
                ('birthday', models.DateField(default=datetime.date(1993, 6, 21))),
                ('password', models.CharField(default='1234', max_length=24)),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.usermanage')),
                ('my_teacher', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='users.teacher')),
            ],
        ),
    ]