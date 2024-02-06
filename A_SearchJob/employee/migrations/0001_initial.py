# Generated by Django 4.2.6 on 2023-10-31 19:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import employee.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=40)),
                ('birth', models.DateField(default='', max_length=10)),
                ('address', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('link_to_own_website', models.URLField(blank=True, default='', null=True)),
                ('linkedin', models.URLField(blank=True, default='', null=True)),
                ('github', models.URLField(blank=True, default='', null=True)),
                ('email', models.EmailField(max_length=40)),
                ('image', models.ImageField(height_field='height_field', upload_to=employee.models.get_path_to_img, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('description_about_yourself', models.TextField(default='')),
                ('level_of_english', models.CharField(choices=[('A1/Elementary', 'A1'), ('A1+/Elementary+', 'A1+'), ('A2/Pre Intermediate', 'A2'), ('A2+/Pre intermediate+', 'A2+'), ('B1/Intermediate', 'B1'), ('B1+/Intermediate+', 'B1+'), ('B2/Upper-intermediate', 'B2'), ('B2+/Upper-intermediate', 'B2+'), ('C1/Advanced', 'C1'), ('C1+/Advanced+', 'C1+'), ('C2/Proficiency', 'C2')], default='B1/Intermediate', max_length=30)),
                ('education', models.TextField(default='')),
                ('hard_skills', models.TextField(default='')),
                ('work_experience', models.TextField(default='')),
                ('main_programming_language', models.CharField(choices=[('1С', '1С'), ('C', 'C'), ('C#/.NET', 'C#/.NET'), ('C++', 'C++'), ('DB langs', 'DB'), ('Dart', 'Dart'), ('Golang', 'Go'), ('Java', 'Java'), ('JavaScript', 'JS'), ('Kotlin', 'Kotlin'), ('PHP', 'PHP'), ('Python', 'Python'), ('Ruby', 'Ruby'), ('Rust', 'Rust'), ('Scala', 'Scala'), ('Swift', 'Swift'), ('TypeScript', 'TypeScript'), ('N/A', 'N/A')], default='Python', max_length=15)),
                ('soft_skills', models.TextField(default='')),
                ('desired_salary', models.SmallIntegerField(default='500')),
                ('additional_files', models.FileField(blank=True, default='', null=True, upload_to='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('type_of_job', models.CharField(choices=[('Intern/Trainee Software Engineer', 'Intern/Trainee SE'), ('Junior Software Engineer', 'Junior SE'), ('Junior+ Software Engineer', 'Junior+ SE'), ('Middle Software Engineer', 'Middle SE'), ('Middle+ Software Engineer', 'Middle+ SE'), ('Senior Software Engineer', 'Senior SE'), ('SE Team/Tech Lead', 'SE Team Lead'), ('System Architect', 'System Architect'), ('Intern/Trainee QA', 'Intern/Trainee QA'), ('Junior QA', 'Junior Qa'), ('Junior+ QA', 'Junior+ QA'), ('Middle QA', 'Middle QA'), ('Middle+ QA', 'Middle+ QA'), ('Senior QA', 'Senior QA'), ('QA Team/Tech Lead', 'QA Team Lead'), ('QA Manager', 'QA Manager'), ('DevOps', 'DevOps'), ('HTML Coder', 'HTML Coder'), ('Security Specialist', 'Security Specialist'), ('Delivery Manager', 'Delivery Manager'), ('Product Manager', 'Product Manager'), ('Product Owner', 'Product Owner'), ('Program Manager', 'Program Manager'), ('Project Manager', 'Project Manager'), ('Data Scientist', 'Data Scientist'), ('Data/Big Data Engineer', 'Data Engineer'), ('Machine Learning Engineer', 'ML Engineer'), ('Business Analyst', 'Business Analyst'), ('Data Analyst', 'Data Analyst'), ('Product Analyst', 'Product Analyst'), ('System Analyst', 'System Analyst')], default='Intern/Trainee Software Engineer', max_length=50)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]