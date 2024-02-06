from django.db import models
from django.conf import settings


def type_of_job():

    variety = [
        ('Intern/Trainee Software Engineer', 'Intern/Trainee Software Engineer'),
        ('Junior Software Engineer', 'Junior Software Engineer'),
        ('Junior+ Software Engineer', 'Junior+ Software Engineer'),
        ('Middle Software Engineer', 'Middle Software Engineer'),
        ('Middle+ Software Engineer', 'Middle+ Software Engineer'),
        ('Senior Software Engineer', 'Senior Software Engineer'),
        ('SE Team/Tech Lead', 'SE Team/Tech Lead'),
        ('System Architect', 'System Architect'),

        ('Intern/Trainee QA', 'Intern/Trainee QA'),
        ('Junior QA', 'Junior QA'),
        ('Junior+ QA', 'Junior+ QA'),
        ('Middle QA', 'Middle QA'),
        ('Middle+ QA', 'Middle+ QA'),
        ('Senior QA', 'Senior QA'),
        ('QA Team/Tech Lead', 'QA Team/Tech Lead'),
        ('QA Manager', 'QA Manager'),

        ('DevOps', 'DevOps'),
        ('HTML Coder', 'HTML Coder'),
        ('Security Specialist', 'Security Specialist'),

        ('Delivery Manager', 'Delivery Manager'),
        ('Product Manager', 'Product Manager'),
        ('Product Owner', 'Product Owner'),
        ('Program Manager', 'Program Manager'),
        ('Project Manager', 'Project Manager'),

        ('Data Scientist', 'Data Scientist'),
        ('Data/Big Data Engineer', 'Data/Big Data Engineer'),
        ('Machine Learning Engineer', 'Machine Learning Engineer'),

        ('Business Analyst', 'Business Analyst'),
        ('Data Analyst', 'Data Analyst'),
        ('Product Analyst', 'Product Analyst'),
        ('System Analyst', 'System Analyst')
    ]

    return variety


def level_of_eng():

    levels = [
        ('A1/Elementary', 'A1/Elementary'),
        ('A1+/Elementary+', 'A1+/Elementary+'),
        ('A2/Pre Intermediate', 'A2/Pre Intermediate'),
        ('A2+/Pre intermediate+', 'A2+/Pre intermediate+'),
        ('B1/Intermediate', 'B1/Intermediate'),
        ('B1+/Intermediate+', 'B1+/Intermediate+'),
        ('B2/Upper-intermediate', 'B2/Upper-intermediate'),
        ('B2+/Upper-intermediate', 'B2+/Upper-intermediate'),
        ('C1/Advanced', 'C1/Advanced'),
        ('C1+/Advanced+', 'C1+/Advanced+'),
        ('C2/Proficiency', 'C2/Proficiency')
    ]

    return levels


def programming_languages():

    languages = [
        ('1С', '1С'),
        ('C', 'C'),
        ('C#/.NET', 'C#/.NET'),
        ('C++', 'C++'),
        ('DB langs', 'DB langs'),
        ('Dart', 'Dart'),
        ('Golang', 'Golang'),
        ('Java', 'Java'),
        ('JavaScript', 'JavaScript'),
        ('Kotlin', 'Kotlin'),
        ('PHP', 'PHP'),
        ('Python', 'Python'),
        ('Ruby', 'Ruby'),
        ('Rust', 'Rust'),
        ('Scala', 'Scala'),
        ('Swift', 'Swift'),
        ('TypeScript', 'TypeScript'),
        ('N/A', 'N/A')
    ]

    return languages


def time_work():

    variety = [
        ('Full-time job', 'Full-time job'),
        ('Part-time job', 'Part-time job')
    ]

    return variety


class EmployerModel(models.Model):

    name_of_job = models.CharField(max_length=100, default='')
    location = models.CharField(max_length=50, default='')
    name_of_company = models.CharField(max_length=50, default='')

    required_english = models.CharField(choices=level_of_eng(), default=level_of_eng()[4][0], max_length=30)
    type_of_job = models.CharField(max_length=40, choices=type_of_job(), default=type_of_job()[0][0])
    main_programming_language = models.CharField(max_length=15, choices=programming_languages(),
                                                 default=programming_languages()[11][0])

    lower_salary = models.SmallIntegerField(default=500)
    higher_salary = models.SmallIntegerField(default=1000)

    remote_job = models.BooleanField(default=False)
    min_experience = models.SmallIntegerField(default=0)

    benefits_of_job = models.TextField(default='')
    responsibilities_of_job = models.TextField(default='')
    requirements_of_job = models.TextField(default='')

    link_to_own_website = models.URLField(default='', null=True, blank=True)
    linkedin = models.URLField(default='', null=True, blank=True)
    email = models.EmailField(max_length=40, default='')
    phone_number = models.CharField(max_length=20, default='')

    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        on_delete=models.PROTECT
    )

    time_work = models.CharField(choices=time_work(), default=time_work()[0][0], max_length=15)

    class Meta:
        ordering = ('-timestamp', '-name_of_job')
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'

    def get_url_to_vacancy(self):
        return f'/{settings.USER_SIDE}/vacancy/{self.id}/'

    def get_url_to_update_vacancy(self):
        return f'/{settings.USER_SIDE}/update/{self.id}/'

    def __str__(self):
        return f'{self.name_of_company}---{self.name_of_job}'
