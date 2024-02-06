from django.db import models
from django.conf import settings


def get_path_to_img(user, filename):
    return f'{user.id}, {filename}'


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


class EmployeeModel(models.Model):
    name = models.CharField(max_length=40, default='')
    birth = models.DateField(default='', max_length=10)

    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)

    link_to_own_website = models.URLField(default='', null=True, blank=True)
    linkedin = models.URLField(default='', null=True, blank=True)
    github = models.URLField(default='', null=True, blank=True)
    email = models.EmailField(max_length=40)

    image = models.ImageField(null=True, blank=True,
                              width_field='width_field',
                              height_field='height_field',
                              upload_to=get_path_to_img)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    description_about_yourself = models.TextField(default='')

    level_of_english = models.CharField(max_length=30, choices=level_of_eng(), default=level_of_eng()[4][0])

    education = models.TextField(default='')
    hard_skills = models.TextField(default='')
    work_experience = models.TextField(default='')
    main_programming_language = models.CharField(max_length=15, choices=programming_languages(),
                                                 default=programming_languages()[11][0])

    soft_skills = models.TextField(default='')
    desired_salary = models.PositiveSmallIntegerField(default='500')

    additional_files = models.FileField(default='', null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    type_of_job = models.CharField(max_length=50, choices=type_of_job(), default=type_of_job()[0][0])

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ('-timestamp', 'name')
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'

    def __str__(self):
        return f'{self.name}---{self.birth}'

    def get_url_to_resume(self):
        return f'/employee/update/{self.id}/'

    def get_url_to_whole_resume(self):
        return f'/{settings.USER_SIDE}/resume/{self.id}/'
