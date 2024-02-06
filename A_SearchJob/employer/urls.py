from django.urls import path
from employer.views import home, create_vacancy, update_vacancy, delete_vacancy, \
    liked_resumes, own_vacancies, resume, vacancy, like_resume, respond_to_resume

app_name = 'employer'

urlpatterns = [
    path('', home, name='home-employer'),
    path('create/', create_vacancy, name='create'),
    path('update/<int:id>/', update_vacancy, name='update'),
    path('delete/<int:id>/', delete_vacancy, name='delete'),

    path('vacancy/<int:id>/', vacancy, name='vacancy'),
    path('resume/<int:id>/', resume, name='resume'),
    path('like_resume/<int:id>/', like_resume, name='like_resume'),

    path('liked/', liked_resumes, name='liked'),
    path('vacancies/', own_vacancies, name='vacancies'),

    path('respond/<int:id>/', respond_to_resume, name='respond')
]
