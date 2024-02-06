from django.shortcuts import render, get_object_or_404, redirect
from additional_functions.additional import paginator_array, split_lines, set_width_height_for_image, get_current_year

from employee.models import EmployeeModel
from employer.models import EmployerModel
from users.models import User

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from employer.forms import EmployerForm

from django.contrib import messages
from django.conf import settings

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import json


def home(request):

    settings.USER_SIDE = 'employer'

    queryset = EmployeeModel.objects.all()

    query = request.GET.get('q_resumes')
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(main_programming_language__icontains=query) |
            Q(type_of_job__icontains=query) |
            Q(address__icontains=query) |
            Q(hard_skills__icontains=query)
        )

    resumes_per_page = 4
    paginator = Paginator(queryset, resumes_per_page)

    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.get_page(page)
    except PageNotAnInteger:
        queryset = paginator.page(paginator.num_pages)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        'resumes': queryset,
        'page_request_var': page_request_var,
        'paginator_range': paginator_array(paginator.num_pages, paginator.get_page(page).number),
        'count_of_pages': paginator.num_pages,
        'count_of_resumes': len(queryset),
        'current_year': get_current_year()
    }

    return render(request, 'employer/home.html', context)


def create_vacancy(request):
    form = EmployerForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        vacancy_ins = form.save(commit=False)
        vacancy_ins.user = request.user
        vacancy_ins.save()

        extra_tags = 'html_safe'

        message = f'<p>The <a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/employer/vacancy/{vacancy_ins.id}/">vacancy</a> was successfully created!</p>' \
                  f'<p>To update your vacancy, click <a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/employer/update/{vacancy_ins.id}/">here</a></p>'

        messages.info(request, message, extra_tags)

        return redirect('employer:vacancies')

    context = {
        'form': form,
        'text_for_btn': 'Create vacancy',
        'remote_job': '',
        'current_year': get_current_year(),
    }

    return render(request, 'employer/vacancy_creation.html', context)


def update_vacancy(request, id=None):

    vacancy_ins = get_object_or_404(EmployerModel, id=id)
    form = EmployerForm(request.POST or None, request.FILES or None, instance=vacancy_ins)

    if form.is_valid():
        vacancy_ins = form.save(commit=False)
        vacancy_ins.save()

        extra_tags = 'html_safe'

        message = f'<p>The <a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/employer/vacancy/{vacancy_ins.id}/">vacancy</a> was successfully updated!</p>' \
                  f'<p>To update again your vacancy, click <a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/employer/update/{vacancy_ins.id}/">here</a></p>'

        messages.info(request, message, extra_tags)

        return redirect('employer:vacancies')

    context = {
        'form': form,
        'text_for_btn': 'Update vacancy',
        'remote_job': vacancy_ins.remote_job,
        'current_year': get_current_year()
    }

    return render(request, 'employer/vacancy_creation.html', context)


def delete_vacancy(request, id=None):
    vacancy_instance = get_object_or_404(EmployerModel, id=id)
    vacancy_instance.delete()

    extra_tags = 'html_safe'
    message = f'<p>Vacancy has just been successfully deleted!</p>'

    messages.info(request, message, extra_tags)

    return redirect('employer:vacancies')


def like_resume(request, id=None):

    resume_obj = get_object_or_404(EmployeeModel, id=id)

    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)

        user_id = str(user.id)
        resume_id = resume_obj.id

        with open('additional_files/liked_resumes.json', "r") as file:
            data = json.load(file)

        if user_id in data['users']:
            if resume_id in data['users'][user_id]:
                data['users'][user_id].remove(resume_id)
            else:
                data['users'][user_id].append(resume_id)
        else:
            data['users'][user_id] = [resume_id]

        with open('additional_files/liked_resumes.json', 'w') as file:
            json.dump(data, file)

    return redirect(f'/employer/resume/{resume_obj.id}/')


def resume(request, id=None):

    resume_obj = get_object_or_404(EmployeeModel, id=id)
    size_of_image = set_width_height_for_image(resume_obj.width_field, resume_obj.height_field)

    context = {
        'resume': resume_obj,
        'image_width': size_of_image[0],
        'image_height': size_of_image[1],
        'soft_skills': split_lines(resume_obj.soft_skills),
        'hard_skills': split_lines(resume_obj.hard_skills),
        'user': request.user,
        'current_year': get_current_year()
    }

    if resume_obj.image:
        context['image_existence'] = True
    else:
        context['image_existence'] = False

    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        context['user_main'] = user

        with open('additional_files/liked_resumes.json', "r") as file:
            data = json.load(file)

        user_id = str(user.id)

        try:
            if resume_obj.id in data['users'][user_id]:
                context['existence_in_liked_resumes'] = True
            else:
                context['existence_in_liked_resumes'] = False
        except KeyError:
            context['existence_in_liked_resumes'] = False

    return render(request, 'employer/resume.html', context)


def own_vacancies(request):
    queryset = [vacancy for vacancy in EmployerModel.objects.all() if vacancy.user == request.user]

    context = {
        'vacancies': queryset,
        'count_of_vacancies': len(queryset),
        'current_year': get_current_year()
    }

    return render(request, 'employer/own_vacancies.html', context)


def vacancy(request, id=None):

    vacancy_obj = get_object_or_404(EmployerModel, id=id)

    context = {
        'vacancy': vacancy_obj,
        'user': request.user,
        'requirements': split_lines(vacancy_obj.requirements_of_job),
        'benefits': split_lines(vacancy_obj.benefits_of_job),
        'responsibilities': split_lines(vacancy_obj.responsibilities_of_job),
        'current_year': get_current_year()
    }

    return render(request, 'employer/vacancy.html', context)


def liked_resumes(request):

    user = get_object_or_404(User, id=request.user.id)

    with open('additional_files/liked_resumes.json', "r") as file:
        data = json.load(file)

    user_id = str(user.id)

    try:
        liked_resumes_user = data['users'][user_id]
        queryset = EmployeeModel.objects.all().filter(id__in=liked_resumes_user)
    except KeyError:
        queryset = EmployeeModel.objects.all().filter(id__in=[0])

    query = request.GET.get('q_liked_r')
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(main_programming_language__icontains=query) |
            Q(type_of_job__icontains=query) |
            Q(address__icontains=query) |
            Q(hard_skills__icontains=query)
        )

    context = {
        'resumes': queryset,
        'count_of_resumes': len(queryset),
        'add_query': False,
        'current_year': get_current_year()
    }

    if query:
        context['add_query'] = True
    else:
        context['add_query'] = False

    return render(request, 'employer/liked_resumes.html', context)


def respond_to_resume(request, id=None):

    if not request.user.is_authenticated:
        return redirect('users:login')

    resume_obj = get_object_or_404(EmployeeModel, id=id)
    user_obj = get_object_or_404(User, id=request.user.id)

    queryset_of_appropriate_vacancies = EmployerModel.objects.all().filter(user=user_obj)
    number_of_vacancies = len(queryset_of_appropriate_vacancies)

    subject = 'Response to the resume'
    from_email = settings.EMAIL_HOST_USER
    to = resume_obj.email

    # for local site
    prefix_for_url = 'http://127.0.0.1:8000'

    context_for_email = {
        'subject': subject,
        'resume': resume_obj,
        'vacancies': queryset_of_appropriate_vacancies,
        'number_of_vacancies': number_of_vacancies,
        'prefix': prefix_for_url
    }

    if queryset_of_appropriate_vacancies:
        id_for_vacancy = [obj_id.id for obj_id in queryset_of_appropriate_vacancies]
        emails = list(set([obj.email for obj in queryset_of_appropriate_vacancies]))
        phone_numbers = list(set([obj.phone_number for obj in queryset_of_appropriate_vacancies]))

        if number_of_vacancies == 1:
            context_for_email['id_for_vacancy'] = id_for_vacancy[0]
            context_for_email['email'] = emails[0]
            context_for_email['phone_number'] = phone_numbers[0]
        else:
            context_for_email['id_for_vacancy'] = id_for_vacancy
            context_for_email['email'] = emails
            context_for_email['phone_number'] = phone_numbers

    html_content = render_to_string('employer/email_content.html', context_for_email)

    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"
    msg.send()

    extra_tags = 'html_safe'

    message = "An email with your information has been sent to the resume owner's email address. " \
              "Wait for answer from resume owner. " \
              "Have a successful agreement!"

    messages.info(request, message, extra_tags)

    return redirect('employer:home-employer')
