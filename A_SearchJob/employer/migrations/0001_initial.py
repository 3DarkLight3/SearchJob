# Generated by Django 4.2.6 on 2023-10-27 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_job', models.CharField(default='', max_length=100)),
                ('location', models.CharField(default='', max_length=50)),
                ('name_of_company', models.CharField(default='', max_length=50)),
                ('required_english', models.CharField(choices=[('A1/Elementary', 'A1'), ('A1+/Elementary+', 'A1+'), ('A2/Pre Intermediate', 'A2'), ('A2+/Pre intermediate+', 'A2+'), ('B1/Intermediate', 'B1'), ('B1+/Intermediate+', 'B1+'), ('B2/Upper-intermediate', 'B2'), ('B2+/Upper-intermediate', 'B2+'), ('C1/Advanced', 'C1'), ('C1+/Advanced+', 'C1+'), ('C2/Proficiency', 'C2')], default=('B1/Intermediate', 'B1'), max_length=30)),
                ('type_of_job', models.CharField(choices=[('Intern/Trainee Software Engineer', 'Intern/Trainee SE'), ('Junior Software Engineer', 'Junior SE'), ('Junior+ Software Engineer', 'Junior+ SE'), ('Middle Software Engineer', 'Middle SE'), ('Middle+ Software Engineer', 'Middle+ SE'), ('Senior Software Engineer', 'Senior SE'), ('SE Team/Tech Lead', 'SE Team Lead'), ('System Architect', 'System Architect'), ('Intern/Trainee QA', 'Intern/Trainee QA'), ('Junior QA', 'Junior Qa'), ('Junior+ QA', 'Junior+ QA'), ('Middle QA', 'Middle QA'), ('Middle+ QA', 'Middle+ QA'), ('Senior QA', 'Senior QA'), ('QA Team/Tech Lead', 'QA Team Lead'), ('QA Manager', 'QA Manager'), ('DevOps', 'DevOps'), ('HTML Coder', 'HTML Coder'), ('Security Specialist', 'Security Specialist'), ('Delivery Manager', 'Delivery Manager'), ('Product Manager', 'Product Manager'), ('Product Owner', 'Product Owner'), ('Program Manager', 'Program Manager'), ('Project Manager', 'Project Manager'), ('Data Scientist', 'Data Scientist'), ('Data/Big Data Engineer', 'Data Engineer'), ('Machine Learning Engineer', 'ML Engineer'), ('Business Analyst', 'Business Analyst'), ('Data Analyst', 'Data Analyst'), ('Product Analyst', 'Product Analyst'), ('System Analyst', 'System Analyst')], default=('Intern/Trainee Software Engineer', 'Intern/Trainee SE'), max_length=40)),
                ('main_programming_language', models.CharField(choices=[('1С', '1С'), ('C', 'C'), ('C#/.NET', 'C#/.NET'), ('C++', 'C++'), ('DB langs', 'DB'), ('Dart', 'Dart'), ('Golang', 'Go'), ('Java', 'Java'), ('JavaScript', 'JS'), ('Kotlin', 'Kotlin'), ('PHP', 'PHP'), ('Python', 'Python'), ('Ruby', 'Ruby'), ('Rust', 'Rust'), ('Scala', 'Scala'), ('Swift', 'Swift'), ('TypeScript', 'TypeScript'), ('N/A', 'N/A')], default=('Python', 'Python'), max_length=15)),
                ('lower_salary', models.SmallIntegerField(default=500)),
                ('higher_salary', models.SmallIntegerField(default=1000)),
                ('remote_job', models.BooleanField(default=False)),
                ('min_experience', models.SmallIntegerField(default=0)),
                ('benefits_of_job', models.TextField(default='')),
                ('responsibilities_of_job', models.TextField(default='')),
                ('requirements_of_job', models.TextField(default='')),
                ('link_to_own_website', models.URLField(blank=True, default='', null=True)),
                ('linkedin', models.URLField(blank=True, default='', null=True)),
                ('email', models.EmailField(default='', max_length=40)),
                ('phone_number', models.CharField(default='', max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]