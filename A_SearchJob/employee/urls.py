from django.urls import path
from employee.views import home, create_resume, update_resume, delete_resume, \
    liked_vacancies, own_resumes, vacancy, resume, like_vacancy, respond_to_vacancy

app_name = 'employee'

urlpatterns = [
    path('', home, name='home-employee'),
    path('create/', create_resume, name='create'),
    path('update/<int:id>/', update_resume, name='update'),
    path('delete/<int:id>/', delete_resume, name='delete'),

    path('liked/', liked_vacancies, name='liked'),
    path('resumes/', own_resumes, name='resumes'),

    path('vacancy/<int:id>/', vacancy, name='vacancy'),
    path('resume/<int:id>/', resume, name='resume'),
    path('like_vacancy/<int:id>/', like_vacancy, name='like_vacancy'),

    path('respond/<int:id>/', respond_to_vacancy, name='respond')
]
